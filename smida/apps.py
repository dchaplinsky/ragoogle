from abstract.apps import AbstractConfig
from .loader import SmidaLoader
from .elastic_models import ElasticSmidaModel, smida_idx


class SmidaConfig(AbstractConfig):
    name = "smida"
    verbose_name = "Власники значної частки СМІДА"
    short_name = "СМІДА"
    loader_class = SmidaLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import SmidaModel
        return SmidaModel
    
    @property
    def sitemap(self):
        from .sitemaps import SmidaSitemap

        return SmidaSitemap

    elastic_model = ElasticSmidaModel
    elastic_index = smida_idx