from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView
from django.utils.translation import gettext as _

from elasticsearch.exceptions import NotFoundError

from .elastic_models import ElasticDataEgovKzGbdUlModel
from .apps import DataEgovKzGbdUlConfig as DataSourceConfig


class DataEgovKzGbdUlDetailsView(TemplateView):
    template_name = "data_egov_kz_gbd_ul/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            rec = ElasticDataEgovKzGbdUlModel.get(id=kwargs["pk"])
        except NotFoundError:
            raise Http404(_("Записа не існує"))

        context["rec"] = rec
        context["datasource"] = DataSourceConfig

        return context
