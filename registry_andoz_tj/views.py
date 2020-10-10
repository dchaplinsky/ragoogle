from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView

from elasticsearch.exceptions import NotFoundError

from .elastic_models import ElasticRegistryAndozTjModel
from .apps import RegistryAndozTjConfig as DataSourceConfig


class RegistryAndozTjDetailsView(TemplateView):
    template_name = "registry_andoz_tj/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            rec = ElasticRegistryAndozTjModel.get(id=kwargs["pk"])
        except NotFoundError:
            raise Http404("Записа не існує")

        context["rec"] = rec
        context["datasource"] = DataSourceConfig

        return context
