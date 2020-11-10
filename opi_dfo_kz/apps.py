from abstract.apps import AbstractConfig
from .loader import OpiDfoKzLoader
from .elastic_models import ElasticOpiDfoKzModel, opi_dfo_kz_idx

from django.utils.translation import gettext_lazy as _

class OpiDfoKzConfig(AbstractConfig):
    name = "opi_dfo_kz"

    verbose_name = _("Депозитарий финансовой отчётности (Казахстан)")
    short_name = _("Финотчётность (kz)")
    loader_class = OpiDfoKzLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import OpiDfoKzModel

        return OpiDfoKzModel

    @property
    def sitemap(self):
        from .sitemaps import OpiDfoKzSitemap

        return OpiDfoKzSitemap

    elastic_model = ElasticOpiDfoKzModel
    elastic_index = opi_dfo_kz_idx
