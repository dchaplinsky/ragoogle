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

TAX_REG_INDEX = "ragoogle_tax_reg"
tax_reg_idx = Index(TAX_REG_INDEX)
tax_reg_idx.settings(**BASIC_INDEX_SETTINGS)


tax_reg_idx.analyzer(namesAutocompleteAnalyzer)
tax_reg_idx.analyzer(namesAutocompleteSearchAnalyzer)
tax_reg_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@tax_reg_idx.doc_type
class ElasticTaxRegModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    def render_infocard(self):
        from .apps import TaxRegConfig as AppConfig

        return render_to_string(
            "tax_reg/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('tax_reg>details', kwargs={'pk': self._id})

    class Meta:
        index = TAX_REG_INDEX
        doc_type = "ragoogle_tax_reg_doctype"
