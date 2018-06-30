from django.apps import AppConfig
from .elastic_models import ElasticMinionModel, minions_idx


class PosipakyInfoConfig(AppConfig):
    name = 'posipaky_info'
    verbose_name = "Помічники народних депутатів"
    elastic_model = ElasticMinionModel
    elastic_index = minions_idx