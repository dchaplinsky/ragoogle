from django.template.loader import render_to_string
from elasticsearch_dsl import Keyword
from django.urls import reverse

from abstract.elastic_models import (
    BASIC_INDEX_SETTINGS,
    AbstractDatasetMapping,
    namesAutocompleteAnalyzer,
    namesAutocompleteSearchAnalyzer,
    ukrainianAddressesStopwordsAnalyzer,
)
from elasticsearch_dsl import DocType, Index, Text, Keyword

GR5_GOSREESTR_KZ_INDEX = "ragoogle_gr5_gosreestr_kz"
gr5_gosreestr_kz_idx = Index(GR5_GOSREESTR_KZ_INDEX)
gr5_gosreestr_kz_idx.settings(**BASIC_INDEX_SETTINGS)


gr5_gosreestr_kz_idx.analyzer(namesAutocompleteAnalyzer)
gr5_gosreestr_kz_idx.analyzer(namesAutocompleteSearchAnalyzer)
gr5_gosreestr_kz_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@gr5_gosreestr_kz_idx.doc_type
class ElasticGr5GosreestrKzModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    companies = Text(copy_to="all")
    raw_records = Text(copy_to="all")
    all = Text()

    def render_infocard(self):
        from .apps import Gr5GosreestrKzConfig as AppConfig

        return render_to_string(
            "gr5_gosreestr_kz/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('gr5_gosreestr_kz>details', kwargs={'pk': self._id})

    class Meta:
        index = GR5_GOSREESTR_KZ_INDEX
        doc_type = "ragoogle_gr5_gosreestr_kz_doctype"
