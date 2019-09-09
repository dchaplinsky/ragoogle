from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView

from elasticsearch.exceptions import NotFoundError

from .elastic_models import ElasticSmidaModel
from .apps import SmidaConfig as DataSourceConfig


class SmidaDetailsView(TemplateView):
    template_name = "smida/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            rec = ElasticSmidaModel.get(id=kwargs["pk"])
        except NotFoundError:
            raise Http404("Записа не існує")

        context["rec"] = rec
        context["datasource"] = DataSourceConfig

        return context
