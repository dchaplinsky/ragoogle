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

CVK2015_INDEX = "ragoogle_cvk_2015"
cvk_2015_idx = Index(CVK2015_INDEX)
cvk_2015_idx.settings(**BASIC_INDEX_SETTINGS)


cvk_2015_idx.analyzer(namesAutocompleteAnalyzer)
cvk_2015_idx.analyzer(namesAutocompleteSearchAnalyzer)
cvk_2015_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@cvk_2015_idx.doc_type
class ElasticCVK2015Model(AbstractDatasetMapping):
    def render_infocard(self):
        from .apps import CVK2015Config as AppConfig

        return render_to_string(
            "cvk_2015/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('cvk_2015>details', kwargs={'pk': self._id})

    class Meta:
        index = CVK2015_INDEX
        doc_type = "ragoogle_cvk_2015_doctype"
