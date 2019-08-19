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

CORRUPT_INDEX = "ragoogle_corrupt"
corrupt_idx = Index(CORRUPT_INDEX)
corrupt_idx.settings(**BASIC_INDEX_SETTINGS)


corrupt_idx.analyzer(namesAutocompleteAnalyzer)
corrupt_idx.analyzer(namesAutocompleteSearchAnalyzer)
corrupt_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@corrupt_idx.doc_type
class ElasticCorruptModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    def render_infocard(self):
        from .apps import CorruptConfig as AppConfig

        return render_to_string(
            "corrupt/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('corrupt>details', kwargs={'pk': self._id})

    class Meta:
        index = CORRUPT_INDEX
        doc_type = "ragoogle_corrupt_doctype"
