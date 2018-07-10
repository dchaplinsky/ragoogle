from django.apps import AppConfig
from .elastic_models import ElasticVKKSModel, vkks_idx
from .loader import VKKSLoader


class VKKSConfig(AppConfig):
    name = 'vkks'
    verbose_name = "Декларації родинних зв'язків суддів та кандидатів"
    loader_class = VKKSLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import VKKSModel
        return VKKSModel
    
    elastic_model = ElasticVKKSModel
    elastic_index = vkks_idx