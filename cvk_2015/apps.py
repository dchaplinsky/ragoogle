from django.apps import AppConfig
from .loader import CVK2015Loader
from .elastic_models import ElasticCVK2015Model, cvk_2015_idx


class CVK2015Config(AppConfig):
    name = "cvk_2015"
    verbose_name = "Учасники місцевих виборів 2015-го року"
    loader_class = CVK2015Loader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import CVK2015Model
        return CVK2015Model
    
    @property
    def sitemap(self):
        from .sitemaps import CVK2015Sitemap

        return CVK2015Sitemap

    elastic_model = ElasticCVK2015Model
    elastic_index = cvk_2015_idx