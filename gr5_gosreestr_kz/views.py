from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView
from django.utils.translation import gettext as _

from elasticsearch.exceptions import NotFoundError

from .elastic_models import ElasticGr5GosreestrKzModel
from .apps import Gr5GosreestrKzConfig as DataSourceConfig


class Gr5GosreestrKzDetailsView(TemplateView):
    template_name = "gr5_gosreestr_kz/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            rec = ElasticGr5GosreestrKzModel.get(id=kwargs["pk"])
        except NotFoundError:
            raise Http404(_("Записа не існує"))

        context["rec"] = rec
        context["datasource"] = DataSourceConfig

        return context
