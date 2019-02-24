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

COMPANY_HOUSE_UA_INDEX = "ragoogle_company_house_ua"
company_house_ua_idx = Index(COMPANY_HOUSE_UA_INDEX)
company_house_ua_idx.settings(**BASIC_INDEX_SETTINGS)


company_house_ua_idx.analyzer(namesAutocompleteAnalyzer)
company_house_ua_idx.analyzer(namesAutocompleteSearchAnalyzer)
company_house_ua_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@company_house_ua_idx.doc_type
class ElasticCompanyHouseUaModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    def render_infocard(self):
        from .apps import CompanyHouseUaConfig as AppConfig

        return render_to_string(
            "company_house_ua/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('company_house_ua>details', kwargs={'pk': self._id})

    class Meta:
        index = COMPANY_HOUSE_UA_INDEX
        doc_type = "ragoogle_company_house_ua_doctype"
