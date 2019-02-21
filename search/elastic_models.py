from django.conf import settings

from abstract.elastic_models import BASIC_INDEX_SETTINGS

from elasticsearch_dsl import DocType, Keyword, Text, Index



NAMES_INDEX = "ragoogle_aux_names"
names_idx = Index(NAMES_INDEX)
names_idx.settings(**BASIC_INDEX_SETTINGS)


class Names(DocType):
    """Names document."""
    name = Keyword(index=True, copy_to="all")
    all = Text(analyzer='ukrainian')


    class Meta:
        index = NAMES_INDEX
        doc_type = "ragoogle_aux_names_doctype"
