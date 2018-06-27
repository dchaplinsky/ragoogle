from django.apps import AppConfig
from .loader import SmidaLoader
from .elastic_models import ElasticSmidaModel, smida_idx


class SmidaConfig(AppConfig):
    name = "smida"
    verbose_name = "Власники значної частки СМІДА"
    loader_class = SmidaLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import SmidaModel
        return SmidaModel
    
    elastic_model = ElasticSmidaModel
    elastic_index = smida_idx