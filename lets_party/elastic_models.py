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

LETS_PARTY_INDEX = "ragoogle_lets_party"
lets_party_idx = Index(LETS_PARTY_INDEX)
lets_party_idx.settings(**BASIC_INDEX_SETTINGS)


lets_party_idx.analyzer(namesAutocompleteAnalyzer)
lets_party_idx.analyzer(namesAutocompleteSearchAnalyzer)
lets_party_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@lets_party_idx.doc_type
class ElasticLetsPartyModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    def render_infocard(self):
        from .apps import LetsPartyConfig as AppConfig

        return render_to_string(
            "lets_party/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('lets_party>details', kwargs={'pk': self._id})

    class Meta:
        index = LETS_PARTY_INDEX
        doc_type = "ragoogle_lets_party_doctype"
