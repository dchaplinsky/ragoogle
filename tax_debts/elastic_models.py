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

TAX_DEBTS_INDEX = "ragoogle_tax_debts"
tax_debts_idx = Index(TAX_DEBTS_INDEX)
tax_debts_idx.settings(**BASIC_INDEX_SETTINGS)


tax_debts_idx.analyzer(namesAutocompleteAnalyzer)
tax_debts_idx.analyzer(namesAutocompleteSearchAnalyzer)
tax_debts_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@tax_debts_idx.doc_type
class ElasticTaxDebtsModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    def render_infocard(self):
        from .apps import TaxDebtsConfig as AppConfig

        return render_to_string(
            "tax_debts/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('tax_debts>details', kwargs={'pk': self._id})

    class Meta:
        index = TAX_DEBTS_INDEX
        doc_type = "ragoogle_tax_debts_doctype"
