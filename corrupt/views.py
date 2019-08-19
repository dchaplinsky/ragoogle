from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView

from elasticsearch.exceptions import NotFoundError

from .elastic_models import ElasticCorruptModel


class CorruptDetailsView(TemplateView):
    template_name = "corrupt/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            rec = ElasticCorruptModel.get(id=kwargs["pk"])
        except NotFoundError:
            raise Http404("Записа не існує")

        context["rec"] = rec

        return context
