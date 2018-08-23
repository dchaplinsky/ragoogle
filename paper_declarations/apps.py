from django.apps import AppConfig
from .elastic_models import ElasticPaperDeclarationModel, paper_declaration_idx


class PaperDeclarationsConfig(AppConfig):
    name = 'paper_declarations'
    verbose_name = "Паперові декларації"
    elastic_model = ElasticPaperDeclarationModel
    elastic_index = paper_declaration_idx
