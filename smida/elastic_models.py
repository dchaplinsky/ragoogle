from abstract.elastic_models import (
    BASIC_INDEX_SETTINGS,
    AbstractDatasetMapping,
    namesAutocompleteAnalyzer,
    namesAutocompleteSearchAnalyzer,
    ukrainianAddressesStopwordsAnalyzer
)
from elasticsearch_dsl import DocType, Index

SMIDA_INDEX = "ragoogle_smida"
smida_idx = Index(SMIDA_INDEX)
smida_idx.settings(**BASIC_INDEX_SETTINGS)


smida_idx.analyzer(namesAutocompleteAnalyzer)
smida_idx.analyzer(namesAutocompleteSearchAnalyzer)
smida_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@smida_idx.doc_type
class ElasticSmidaModel(AbstractDatasetMapping):
    pass
