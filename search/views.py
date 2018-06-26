from collections import defaultdict

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.shortcuts import render

from elasticsearch_dsl import Search, Q

from search.search_tools import get_all_enabled_indices, get_all_enabled_models

class HomeView(TemplateView):
    template_name = "search/home.html"


class SearchView(TemplateView):
    template_name = "search/search.html"


class SuggestView(View):
    def get(self, request):
        q = request.GET.get('q', '').strip()

        suggestions = []
        seen = set()

        s = Search(index=get_all_enabled_indices()).doc_type(
            *get_all_enabled_models()
        ).source(
            ['names_autocomplete']
        ).highlight('names_autocomplete').highlight_options(
            order='score', fragment_size=100,
            number_of_fragments=10,
            pre_tags=['<strong>'],
            post_tags=["</strong>"]
        )

        s = s.query(
            "bool",
            must=[
                Q(
                    "match",
                    names_autocomplete={
                        "query": q,
                        "operator": "and"
                    }
                )
            ],
            should=[
                Q(
                    "match_phrase",
                    names_autocomplete__raw={
                        "query": q,
                        "boost": 2
                    },
                ),
                Q(
                    "match_phrase_prefix",
                    names_autocomplete__raw={
                        "query": q,
                        "boost": 2
                    },
                )
            ]
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
            render_to_string("search/autocomplete.html", {
                "result": {
                    "hl": k
                }
            })
            for k in suggestions[:20]
        ]

        return JsonResponse(rendered_result, safe=False)
