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

SMIDA_INDEX = "ragoogle_smida"
smida_idx = Index(SMIDA_INDEX)
smida_idx.settings(**BASIC_INDEX_SETTINGS)


smida_idx.analyzer(namesAutocompleteAnalyzer)
smida_idx.analyzer(namesAutocompleteSearchAnalyzer)
smida_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@smida_idx.doc_type
class ElasticSmidaModel(AbstractDatasetMapping):
    def render_infocard(self):
        from .apps import SmidaConfig as AppConfig

        return render_to_string(
            "smida/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('smida>details', kwargs={'pk': self._id})

    class Meta:
        index = SMIDA_INDEX
        doc_type = "ragoogle_smida_doctype"
