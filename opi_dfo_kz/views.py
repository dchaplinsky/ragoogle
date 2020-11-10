from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView
from django.utils.translation import gettext as _

from elasticsearch.exceptions import NotFoundError

from .elastic_models import ElasticOpiDfoKzModel
from .apps import OpiDfoKzConfig as DataSourceConfig


class OpiDfoKzDetailsView(TemplateView):
    template_name = "opi_dfo_kz/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            rec = ElasticOpiDfoKzModel.get(id=kwargs["pk"])
        except NotFoundError:
            raise Http404(_("Записа не існує"))

        context["rec"] = rec
        context["datasource"] = DataSourceConfig

        return context
