from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView

from elasticsearch.exceptions import NotFoundError

from .elastic_models import ElasticVKKSModel
from .apps import VKKSConfig as DataSourceConfig


class VKKSDetailsView(TemplateView):
    template_name = "vkks/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            rec = ElasticVKKSModel.get(id=kwargs["pk"])
        except NotFoundError:
            raise Http404("Записа не існує")

        context["rec"] = rec
        context["datasource"] = DataSourceConfig

        return context


class VKKSHomeView(TemplateView):
    template_name = "vkks/home.html"
