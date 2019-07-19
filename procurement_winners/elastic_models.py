from django.template.loader import render_to_string
from elasticsearch_dsl import Keyword, Date
from django.urls import reverse

from abstract.elastic_models import (
    BASIC_INDEX_SETTINGS,
    AbstractDatasetMapping,
    namesAutocompleteAnalyzer,
    namesAutocompleteSearchAnalyzer,
    ukrainianAddressesStopwordsAnalyzer,
)
from elasticsearch_dsl import DocType, Index

PROCUREMENT_WINNERS_INDEX = "ragoogle_procurement_winners"
procurement_winners_idx = Index(PROCUREMENT_WINNERS_INDEX)
procurement_winners_idx.settings(**BASIC_INDEX_SETTINGS)


procurement_winners_idx.analyzer(namesAutocompleteAnalyzer)
procurement_winners_idx.analyzer(namesAutocompleteSearchAnalyzer)
procurement_winners_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@procurement_winners_idx.doc_type
class ElasticProcurementWinnersModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    accept_date = Date()
    announce_date = Date()
    date = Date()
    source = Keyword()

    def render_infocard(self):
        from .apps import ProcurementWinnersConfig as AppConfig

        return render_to_string(
            "procurement_winners/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('procurement_winners>details', kwargs={'pk': self._id})

    class Meta:
        index = PROCUREMENT_WINNERS_INDEX
        doc_type = "ragoogle_procurement_winners_doctype"
