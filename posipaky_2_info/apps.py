from django.apps import AppConfig
from .elastic_models import ElasticMinion2Model, minions2_idx


class Posipaky2InfoConfig(AppConfig):
    name = 'posipaky_2_info'
    verbose_name = "Помічника міських депутатів"
    elastic_model = ElasticMinion2Model
    elastic_index = minions2_idx