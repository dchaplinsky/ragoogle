from django.apps import AppConfig
from .elastic_models import ElasticEDRDRModel, edrdr_idx


class EDRDRConfig(AppConfig):
    name = 'edrdr'
    verbose_name = "Єдиний державний реєстр юросіб (ЄДР)"
    elastic_model = ElasticEDRDRModel
    elastic_index = edrdr_idx
