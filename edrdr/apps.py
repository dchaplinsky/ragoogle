from abstract.apps import AbstractConfig
from .elastic_models import ElasticEDRDRModel, edrdr_idx


class EDRDRConfig(AbstractConfig):
    name = 'edrdr'
    verbose_name = "Єдиний державний реєстр юросіб (ЄДР)"
    short_name = "ЄДР"
    elastic_model = ElasticEDRDRModel
    elastic_index = edrdr_idx
