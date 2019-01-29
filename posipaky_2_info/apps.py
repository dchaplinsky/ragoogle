from abstract.apps import AbstractConfig
from .elastic_models import ElasticMinion2Model, minions2_idx


class Posipaky2InfoConfig(AbstractConfig):
    name = 'posipaky_2_info'
    verbose_name = "Помічники місцевих депутатів"
    elastic_model = ElasticMinion2Model
    elastic_index = minions2_idx