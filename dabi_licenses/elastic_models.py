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

DABI_LICENSES_INDEX = "ragoogle_dabi_licenses"
dabi_licenses_idx = Index(DABI_LICENSES_INDEX)
dabi_licenses_idx.settings(**BASIC_INDEX_SETTINGS)


dabi_licenses_idx.analyzer(namesAutocompleteAnalyzer)
dabi_licenses_idx.analyzer(namesAutocompleteSearchAnalyzer)
dabi_licenses_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@dabi_licenses_idx.doc_type
class ElasticDabiLicenseModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    def render_infocard(self):
        from .apps import DabiLicensesConfig as AppConfig

        return render_to_string(
            "dabi_licenses/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('dabi_licenses>details', kwargs={'pk': self._id})

    class Meta:
        index = DABI_LICENSES_INDEX
        doc_type = "ragoogle_dabi_licenses_doctype"
