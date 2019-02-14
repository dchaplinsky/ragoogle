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

GEOINF_LICENSES_INDEX = "ragoogle_geoinf_licenses"
geoinf_licenses_idx = Index(GEOINF_LICENSES_INDEX)
geoinf_licenses_idx.settings(**BASIC_INDEX_SETTINGS)


geoinf_licenses_idx.analyzer(namesAutocompleteAnalyzer)
geoinf_licenses_idx.analyzer(namesAutocompleteSearchAnalyzer)
geoinf_licenses_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@geoinf_licenses_idx.doc_type
class ElasticGeoinfLicenseModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    def render_infocard(self):
        from .apps import GeoinfLicensesConfig as AppConfig

        return render_to_string(
            "geoinf_licenses/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('geoinf_licenses>details', kwargs={'pk': self._id})

    class Meta:
        index = GEOINF_LICENSES_INDEX
        doc_type = "ragoogle_geoinf_licenses_doctype"
