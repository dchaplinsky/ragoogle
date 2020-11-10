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
from elasticsearch_dsl import DocType, Index

OPI_DFO_KZ_INDEX = "ragoogle_opi_dfo_kz"
opi_dfo_kz_idx = Index(OPI_DFO_KZ_INDEX)
opi_dfo_kz_idx.settings(**BASIC_INDEX_SETTINGS)


opi_dfo_kz_idx.analyzer(namesAutocompleteAnalyzer)
opi_dfo_kz_idx.analyzer(namesAutocompleteSearchAnalyzer)
opi_dfo_kz_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@opi_dfo_kz_idx.doc_type
class ElasticOpiDfoKzModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    def render_infocard(self):
        from .apps import OpiDfoKzConfig as AppConfig

        return render_to_string(
            "opi_dfo_kz/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('opi_dfo_kz>details', kwargs={'pk': self._id})

    class Meta:
        index = OPI_DFO_KZ_INDEX
        doc_type = "ragoogle_opi_dfo_kz_doctype"
