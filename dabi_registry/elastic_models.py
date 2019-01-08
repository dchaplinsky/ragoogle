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

DABI_REGISTRY_INDEX = "ragoogle_dabi_registry"
dabi_registry_idx = Index(DABI_REGISTRY_INDEX)
dabi_registry_idx.settings(**BASIC_INDEX_SETTINGS)


dabi_registry_idx.analyzer(namesAutocompleteAnalyzer)
dabi_registry_idx.analyzer(namesAutocompleteSearchAnalyzer)
dabi_registry_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@dabi_registry_idx.doc_type
class ElasticDabiRegistryModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    def render_infocard(self):
        from .apps import DabiRegistryConfig as AppConfig

        return render_to_string(
            "dabi_registry/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('dabi_registry>details', kwargs={'pk': self._id})

    class Meta:
        index = DABI_REGISTRY_INDEX
        doc_type = "ragoogle_dabi_registry_doctype"
