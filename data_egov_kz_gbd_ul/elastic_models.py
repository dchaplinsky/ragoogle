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
from elasticsearch_dsl import DocType, Index, Text

DATA_EGOV_KZ_GBD_UL_INDEX = "ragoogle_data_egov_kz_gbd_ul"
data_egov_kz_gbd_ul_idx = Index(DATA_EGOV_KZ_GBD_UL_INDEX)
data_egov_kz_gbd_ul_idx.settings(**BASIC_INDEX_SETTINGS)


data_egov_kz_gbd_ul_idx.analyzer(namesAutocompleteAnalyzer)
data_egov_kz_gbd_ul_idx.analyzer(namesAutocompleteSearchAnalyzer)
data_egov_kz_gbd_ul_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@data_egov_kz_gbd_ul_idx.doc_type
class ElasticDataEgovKzGbdUlModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    addresses = Text(analyzer="ukrainianAddressesStopwordsAnalyzer", copy_to="all")
    companies = Text(copy_to="all")
    persons = Text(copy_to="all")
    raw_records = Text(copy_to="all")
    all = Text()

    def render_infocard(self):
        from .apps import DataEgovKzGbdUlConfig as AppConfig

        return render_to_string(
            "data_egov_kz_gbd_ul/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('data_egov_kz_gbd_ul>details', kwargs={'pk': self._id})

    class Meta:
        index = DATA_EGOV_KZ_GBD_UL_INDEX
        doc_type = "ragoogle_data_egov_kz_gbd_ul_doctype"
