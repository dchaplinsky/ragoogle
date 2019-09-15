import re
from collections import defaultdict, Counter, OrderedDict

from django.db.models import Max, Min
from django.http import JsonResponse, Http404
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage
from django.shortcuts import render

from elasticsearch_dsl import Search, Q, MultiSearch

from search.search_tools import (
    get_all_enabled_indices,
    get_all_enabled_models,
    get_all_enabled_datasources,
    get_all_doctypes,
)

from search.paginator import paginated
from search.api import serialize_for_api
from search.models import DataSource
from edrdr.elastic_models import ElasticEDRDRModel


class HomeView(TemplateView):
    template_name = "search/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({"datasources": get_all_enabled_datasources().values()})

        return context


class SuggestView(View):
    def merge_sources(self, sources):
        if not sources:
            return []

        models = get_all_doctypes()

        res = []
        seen = OrderedDict()
        for s in sources:
            if s in models:
                model = models.get(s)
                seen.setdefault(model.short_name, []).append(model.name)

        return seen

    def get(self, request):
        q = request.GET.get("q", "").strip()

        suggestions = []
        max_suggestions = 20

        base_q = Search(
            index=get_all_enabled_indices(request.GET.getlist("datasources"))
        ).doc_type(*get_all_enabled_models())

        s = base_q.highlight("names_autocomplete").highlight_options(
            order="score",
            fragment_size=100,
            number_of_fragments=10,
            pre_tags=["<strong>"],
            post_tags=["</strong>"],
        )

        s = s.query(
            "bool",
            must=[Q("match", names_autocomplete={"query": q, "operator": "and"})],
            should=[
                Q("match_phrase", names_autocomplete__raw={"query": q, "boost": 2}),
                Q(
                    "match_phrase_prefix",
                    names_autocomplete__raw={"query": q, "boost": 2},
                ),
            ],
        )[:400]

        res = s.source(False).execute()
        seen = defaultdict(Counter)

        for r in res:
            if "names_autocomplete" in r.meta.highlight:
                for candidate in r.meta.highlight["names_autocomplete"]:

                    if candidate.lower() not in seen:
                        suggestions.append(candidate)
                    seen[candidate.lower()].update([r.meta.doc_type])

        aux_requests_index = []
        aux_requests = MultiSearch()

        suggestions = suggestions[:max_suggestions]

        # Pulling extra info on company names
        aux_results_index = defaultdict(dict)
        if len(q) > 5:
            for k in suggestions:
                sugg = k.replace("<strong>", "").replace("</strong>", "")

                if len(sugg) > 5 and sugg.isdigit():
                    aux_requests_index.append({"key": k, "type": "company"})

                    aux_requests = aux_requests.add(
                        ElasticEDRDRModel.search()
                        .query("match_phrase", all={"query": sugg})
                        .source(["latest_record"])[:1]
                    )

        if aux_requests_index:
            aux_results = aux_requests.execute()

            # Stitching it all together
            for i, r in zip(aux_requests_index, aux_results):
                aux_results_index[i["key"]][i["type"]] = r

        rendered_result = [
            render_to_string(
                "search/autocomplete.html",
                {
                    "request": request,
                    "result": {
                        "hl": k,
                        "q": k.replace("<strong>", "").replace("</strong>", ""),
                        "company_data": aux_results_index[k].get("company", None),
                        "sources_data": self.merge_sources(seen[k.lower()].keys()),
                    },
                },
            )
            for k in suggestions
        ]

        return JsonResponse(rendered_result, safe=False)


class SearchView(TemplateView):
    template_name = "search/search.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        query = request.GET.get("q", "")
        search_type = request.GET.get("search_type", "strict")
        is_addr = request.GET.get("is_addr", "false") == "true"
        entities = request.GET.get("entities", "all")

        if search_type not in ["strict", "loose"]:
            search_type = "strict"

        if entities not in ["all", "addresses", "persons", "companies", "countries"]:
            entities = "all"

        base_q = Search(
            index=get_all_enabled_indices(request.GET.getlist("datasources"))
        ).doc_type(*get_all_enabled_models())

        doctypes = get_all_doctypes()

        if query:
            nwords = len(re.findall(r"\w{2,}", query))

            if nwords > 3:
                should_match = str(nwords - int(nwords > 6) - 1)
            else:
                should_match = "100%"

            if not is_addr:
                clauses = []

                if entities in ["all", "persons"] and nwords >= 3:
                    clauses.append(
                        Q(
                            "match",
                            **{
                                "incomplete_persons": {
                                    "query": query,
                                    "operator": "or",
                                    "minimum_should_match": nwords - 1,
                                }
                            },
                        )
                    )

                compiled_query = Q(
                    "match_phrase", **{entities: {"query": query, "slop": 6}}
                )
                for sub_q in clauses:
                    compiled_query |= sub_q

                strict_query = base_q.query(compiled_query)
            else:
                no_zip_q = re.sub(r"\b\d{5,}\W", "", query)
                strict_query = base_q.query(
                    "match", addresses={"query": no_zip_q, "operator": "and"}
                )

            loose_query = base_q.query(
                "match",
                **{
                    entities: {
                        "query": query,
                        "operator": "or",
                        "minimum_should_match": should_match,
                    }
                },
            )

            ms = MultiSearch()
            ms = ms.add(strict_query[:0])
            ms = ms.add(loose_query[:0])
            sc, lc = ms.execute()

            strict_count = sc.hits.total
            loose_count = lc.hits.total

            if search_type == "loose":
                base_qs = loose_query
                base_count = loose_count
            else:
                base_qs = strict_query
                base_count = strict_count

            qs = base_qs
        else:
            qs = base_q.query("match_all")

            base_count = loose_count = strict_count = qs.count()

        results = qs.highlight_options(
            order="score", pre_tags=['<u class="match">'], post_tags=["</u>"]
        ).highlight(
            "*", require_field_match=False, fragment_size=100, number_of_fragments=10
        )
        results.aggs.bucket("count_by_type", "terms", field="_type")

        search_results = paginated(request, results)

        for res in search_results:
            res.hl = []
            for h_field in getattr(res.meta, "highlight", {}):
                for content in res.meta.highlight[h_field]:
                    res.hl.append(content)

        context.update(
            {
                "search_results": search_results,
                "query": query,
                "search_type": search_type,
                "strict_count": strict_count,
                "loose_count": loose_count,
                "base_count": base_count,
                "enabled_datasources": request.GET.getlist("datasources"),
                "datasources": list(get_all_enabled_datasources().values()),
                "doctypes_mapping": doctypes,
                "foobar": "foobar"
            }
        )

        if request.GET.get("format", "html") == "json":
            del context["view"]
            del context["doctypes_mapping"]
            del context["datasources"]
            if "internals" in context:
                del context["internals"]
            return JsonResponse(serialize_for_api(context), safe=False)
        else:
            return self.render_to_response(context)


class AboutSearchView(TemplateView):
    template_name = "cms/about_search.html"


class AboutAPIView(TemplateView):
    template_name = "cms/about_api.html"


class DataSourceView(DetailView):
    template_name = "search/datasource.html"
    model = DataSource

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datasource = get_all_enabled_datasources().get(context["object"].slug)

        if not datasource:
            raise Http404("Записа не існує")

        context["datasource"] = datasource

        if hasattr(datasource, "data_model"):
            context["rec_count"] = datasource.data_model.objects.count()

            stats = datasource.data_model.objects.aggregate(
                last_updated=Max("last_updated_from_dataset"),
                first_updated=Min("first_updated_from_dataset")
            )

            context.update(stats)
        else:
            context["rec_count"] = datasource.elastic_model.search().count()

        return context