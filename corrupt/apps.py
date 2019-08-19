from abstract.apps import AbstractConfig
from .loader import CorruptLoader
from .elastic_models import ElasticCorruptModel, corrupt_idx


class CorruptConfig(AbstractConfig):
    name = "corrupt"

    verbose_name = "Особи, засуджені за корупцію"
    short_name = "Корупція"
    loader_class = CorruptLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import CorruptModel

        return CorruptModel

    @property
    def sitemap(self):
        from .sitemaps import CorruptSitemap

        return CorruptSitemap

    elastic_model = ElasticCorruptModel
    elastic_index = corrupt_idx
