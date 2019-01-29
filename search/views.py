import re
from collections import defaultdict

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.shortcuts import render

from elasticsearch_dsl import Search, Q, MultiSearch

from search.search_tools import (
    get_all_enabled_indices,
    get_all_enabled_models,
    get_all_enabled_datasources,
)

from search.paginator import paginated
from search.api import serialize_for_api


class HomeView(TemplateView):
    template_name = "search/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({"datasources": get_all_enabled_datasources()})

        return context


class SuggestView(View):
    def get(self, request):
        q = request.GET.get("q", "").strip()

        suggestions = []
        seen = set()

        s = (
            Search(index=get_all_enabled_indices(request.GET.getlist("datasources")))
            .doc_type(*get_all_enabled_models())
            .source(["names_autocomplete"])
            .highlight("names_autocomplete")
            .highlight_options(
                order="score",
                fragment_size=100,
                number_of_fragments=10,
                pre_tags=["<strong>"],
                post_tags=["</strong>"],
            )
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
        )[:200]

        res = s.execute()

        for r in res:
            if "names_autocomplete" in r.meta.highlight:
                for candidate in r.meta.highlight["names_autocomplete"]:
                    if candidate.lower() not in seen:
                        suggestions.append(candidate)
                        seen.add(candidate.lower())

        # Add number of sources where it was found

        rendered_result = [
            render_to_string("search/autocomplete.html", {"result": {"hl": k}})
            for k in suggestions[:20]
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

        if query:
            nwords = len(re.findall(r"\w{2,}", query))

            if nwords > 3:
                should_match = str(nwords - int(nwords > 6) - 1)
            else:
                should_match = "100%"

            if not is_addr:
                strict_query = base_q.query(
                    "match_phrase", **{entities: {"query": query, "slop": 6}}
                )
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
                "datasources": get_all_enabled_datasources(),
            }
        )

        if request.GET.get("format", "html") == "json":
            del context["view"]
            return JsonResponse(serialize_for_api(context), safe=False)
        else:
            return self.render_to_response(context)


class AboutSearchView(TemplateView):
    template_name = "cms/about_search.html"


class AboutAPIView(TemplateView):
    template_name = "cms/about_api.html"
