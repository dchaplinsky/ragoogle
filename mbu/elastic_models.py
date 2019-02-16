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

MBU_INDEX = "ragoogle_mbu"
mbu_idx = Index(MBU_INDEX)
mbu_idx.settings(**BASIC_INDEX_SETTINGS)


mbu_idx.analyzer(namesAutocompleteAnalyzer)
mbu_idx.analyzer(namesAutocompleteSearchAnalyzer)
mbu_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@mbu_idx.doc_type
class ElasticMbuModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    def render_infocard(self):
        from .apps import MbuConfig as AppConfig

        return render_to_string(
            "mbu/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('mbu>details', kwargs={'pk': self._id})

    class Meta:
        index = MBU_INDEX
        doc_type = "ragoogle_mbu_doctype"
