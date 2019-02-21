from abstract.apps import AbstractConfig
from .elastic_models import ElasticMinionModel, minions_idx


class PosipakyInfoConfig(AbstractConfig):
    name = 'posipaky_info'
    short_name = "Рада"
    verbose_name = "Помічники народних депутатів"
    elastic_model = ElasticMinionModel
    elastic_index = minions_idx