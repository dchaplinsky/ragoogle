from abstract.apps import AbstractConfig
from .elastic_models import ElasticVKKSModel, vkks_idx
from .loader import VKKSLoader


class VKKSConfig(AbstractConfig):
    name = "vkks"
    verbose_name = "Декларації родинних зв'язків суддів та кандидатів"
    short_name = "ВККС"
    loader_class = VKKSLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import VKKSModel

        return VKKSModel

    @property
    def sitemap(self):
        from .sitemaps import VKKSSitemap

        return VKKSSitemap

    elastic_model = ElasticVKKSModel
    elastic_index = vkks_idx
