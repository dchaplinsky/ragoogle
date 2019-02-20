from abstract.apps import AbstractConfig
from .elastic_models import ElasticPaperDeclarationModel, paper_declaration_idx


class PaperDeclarationsConfig(AbstractConfig):
    name = 'paper_declarations'
    verbose_name = "Паперові декларації"
    short_name = "НАЗК"
    elastic_model = ElasticPaperDeclarationModel
    elastic_index = paper_declaration_idx
