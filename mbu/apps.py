from abstract.apps import AbstractConfig
from .loader import MbuLoader
from .elastic_models import ElasticMbuModel, mbu_idx


class MbuConfig(AbstractConfig):
    name = "mbu"

    verbose_name = "Містобудівні умови м. Києва"
    short_name = "КГГА"
    loader_class = MbuLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import MbuModel

        return MbuModel

    @property
    def sitemap(self):
        from .sitemaps import MbuSitemap

        return MbuSitemap

    elastic_model = ElasticMbuModel
    elastic_index = mbu_idx
