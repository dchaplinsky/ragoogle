from django.apps import AppConfig
from .elastic_models import ElasticNACPDeclarationModel, nacp_declaration_idx


class NACPDeclarationsConfig(AppConfig):
    name = 'nacp_declarations'
    verbose_name = "Електронні декларації"
    elastic_model = ElasticNACPDeclarationModel
    elastic_index = nacp_declaration_idx
