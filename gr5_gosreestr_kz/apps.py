from abstract.apps import AbstractConfig
from .loader import Gr5GosreestrKzLoader
from .elastic_models import ElasticGr5GosreestrKzModel, gr5_gosreestr_kz_idx

from django.utils.translation import gettext_lazy as _

class Gr5GosreestrKzConfig(AbstractConfig):
    name = "gr5_gosreestr_kz"

    verbose_name = _("Реестр государственных предприятий и учреждений, юридических лиц с участием государства в уставном капитале (Казахстан)")
    short_name = _("Предпр. с гос. капиталом (kz)")

    loader_class = Gr5GosreestrKzLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import Gr5GosreestrKzModel

        return Gr5GosreestrKzModel

    @property
    def sitemap(self):
        from .sitemaps import Gr5GosreestrKzSitemap

        return Gr5GosreestrKzSitemap

    elastic_model = ElasticGr5GosreestrKzModel
    elastic_index = gr5_gosreestr_kz_idx
