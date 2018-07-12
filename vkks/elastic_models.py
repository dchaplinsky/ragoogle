from django.template.loader import render_to_string
from django.urls import reverse

from abstract.elastic_models import (
    BASIC_INDEX_SETTINGS,
    AbstractDatasetMapping,
    namesAutocompleteAnalyzer,
    namesAutocompleteSearchAnalyzer,
    ukrainianAddressesStopwordsAnalyzer,
)
from elasticsearch_dsl import DocType, Index, Text, Keyword, Object

VKKS_INDEX = "ragoogle_vkks"
vkks_idx = Index(VKKS_INDEX)
vkks_idx.settings(**BASIC_INDEX_SETTINGS)


vkks_idx.analyzer(namesAutocompleteAnalyzer)
vkks_idx.analyzer(namesAutocompleteSearchAnalyzer)
vkks_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@vkks_idx.doc_type
class ElasticVKKSModel(AbstractDatasetMapping):
    ID = Keyword(copy_to="all")
    general = Object(
        properties={
            "family_comment": Text(analyzer="ukrainian", copy_to="all"),
            "family_conflicts_comment": Text(analyzer="ukrainian", copy_to="all"),
            "family": Object(
                properties={
                    "career": Object(
                        properties={
                            "position": Text(analyzer="ukrainian", copy_to="all"),
                        }
                    )
                }
            )
        }
    )

    def render_infocard(self):
        from .apps import VKKSConfig as AppConfig

        # TODO: refactor it a bit?
        return render_to_string(
            "vkks/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def get_absolute_url(self):
        return reverse('vkks>details', kwargs={'pk': self._id})

    class Meta:
        index = VKKS_INDEX
        doc_type = "ragoogle_vkks_doctype"
