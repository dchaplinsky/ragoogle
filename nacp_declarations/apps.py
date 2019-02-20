from abstract.apps import AbstractConfig
from .elastic_models import ElasticNACPDeclarationModel, nacp_declaration_idx


class NACPDeclarationsConfig(AbstractConfig):
    name = 'nacp_declarations'
    verbose_name = "Електронні декларації"
    short_name = "НАЗК"
    elastic_model = ElasticNACPDeclarationModel
    elastic_index = nacp_declaration_idx
