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
from elasticsearch_dsl import DocType, Index, Text, Keyword

REGISTRY_ANDOZ_TJ_INDEX = "ragoogle_registry_andoz_tj"
registry_andoz_tj_idx = Index(REGISTRY_ANDOZ_TJ_INDEX)
registry_andoz_tj_idx.settings(**BASIC_INDEX_SETTINGS)


registry_andoz_tj_idx.analyzer(namesAutocompleteAnalyzer)
registry_andoz_tj_idx.analyzer(namesAutocompleteSearchAnalyzer)
registry_andoz_tj_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@registry_andoz_tj_idx.doc_type
class ElasticRegistryAndozTjModel(AbstractDatasetMapping):
    start_date = Keyword()
    end_date = Keyword()

    # Todo: different stopwords
    addresses = Text(analyzer="ukrainianAddressesStopwordsAnalyzer", copy_to="all")
    # Redefining it to remove ukrainian analyzer for now
    persons = Text(copy_to="all")
    countries = Text(copy_to="all")
    companies = Text(copy_to="all")
    raw_records = Text(copy_to="all")
    all = Text()

    def render_infocard(self):
        from .apps import RegistryAndozTjConfig as AppConfig

        return render_to_string(
            "registry_andoz_tj/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('registry_andoz_tj>details', kwargs={'pk': self._id})

    class Meta:
        index = REGISTRY_ANDOZ_TJ_INDEX
        doc_type = "ragoogle_registry_andoz_tj_doctype"
