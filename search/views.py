from django.http import JsonResponse
from django.views import View
from collections import defaultdict
from django.views.generic import TemplateView
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = "search/home.html"


class SearchView(TemplateView):
    template_name = "search/search.html"


class SuggestView(View):
    def get(self, request):
        q = request.GET.get("q", "").strip()

        suggestions = defaultdict(list)
        order_of_suggest = []

        # s = ElasticCompany.search().source(
        #     ['names_autocomplete', "latest_record", "full_edrpou", "companies"]
        # ).highlight('names_autocomplete').highlight_options(
        #     order='score', fragment_size=500,
        #     number_of_fragments=100,
        #     pre_tags=['<strong>'],
        #     post_tags=["</strong>"]
        # )

        # s = s.query(
        #     "bool",
        #     must=[
        #         Q(
        #             "match",
        #             names_autocomplete={
        #                 "query": q,
        #                 "operator": "and"
        #             }
        #         )
        #     ],
        #     should=[
        #         Q(
        #             "match_phrase",
        #             names_autocomplete={
        #                 "query": q,
        #                 "boost": 2
        #             },
        #         ),
        #         Q(
        #             "span_first",
        #             match=Q(
        #                 "span_term",
        #                 names_autocomplete=q
        #             ),
        #             end=4,
        #             boost=2
        #         )
        #     ]
        # )[:200]

        # res = s.execute()
        # for r in res:
        #     if "names_autocomplete" in r.meta.highlight:
        #         for candidate in r.meta.highlight["names_autocomplete"]:
        #             suggestions[candidate.lower()].append((candidate, r))
        #             if candidate.lower() not in order_of_suggest:
        #                 order_of_suggest.append(candidate.lower())

        rendered_result = [
            render_to_string(
                "companies/autocomplete.html", {"suggestion": suggestions[k]}
            )
            for k in order_of_suggest[:20]
        ]

        return JsonResponse(rendered_result, safe=False)
