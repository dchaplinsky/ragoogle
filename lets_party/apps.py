from abstract.apps import AbstractConfig
from .loader import LetsPartyLoader
from .elastic_models import ElasticLetsPartyModel, lets_party_idx


class LetsPartyConfig(AbstractConfig):
    name = "lets_party"

    verbose_name = "Фінансові звіти партій та кандидатів"
    short_name = "Звіти"
    loader_class = LetsPartyLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import LetsPartyModel

        return LetsPartyModel

    @property
    def sitemap(self):
        from .sitemaps import LetsPartySitemap

        return LetsPartySitemap

    elastic_model = ElasticLetsPartyModel
    elastic_index = lets_party_idx
