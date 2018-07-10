from django.template.loader import render_to_string
from django.urls import reverse

from abstract.elastic_models import (
    BASIC_INDEX_SETTINGS,
    AbstractDatasetMapping,
    namesAutocompleteAnalyzer,
    namesAutocompleteSearchAnalyzer,
    ukrainianAddressesStopwordsAnalyzer,
)
from elasticsearch_dsl import DocType, Index

VKKS_INDEX = "ragoogle_vkks"
vkks_idx = Index(VKKS_INDEX)
vkks_idx.settings(**BASIC_INDEX_SETTINGS)


vkks_idx.analyzer(namesAutocompleteAnalyzer)
vkks_idx.analyzer(namesAutocompleteSearchAnalyzer)
vkks_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@vkks_idx.doc_type
class ElasticVKKSModel(AbstractDatasetMapping):
    def render_infocard(self):
        from .apps import SmidaConfig as AppConfig

        # TODO: refactor it a bit?
        return render_to_string(
            "vkks/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    class Meta:
        index = VKKS_INDEX
        doc_type = "ragoogle_smida_doctype"
