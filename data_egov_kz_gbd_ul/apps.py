from abstract.apps import AbstractConfig
from .loader import DataEgovKzGbdUlLoader
from .elastic_models import ElasticDataEgovKzGbdUlModel, data_egov_kz_gbd_ul_idx

from django.utils.translation import gettext_lazy as _

class DataEgovKzGbdUlConfig(AbstractConfig):
    name = "data_egov_kz_gbd_ul"

    verbose_name = _("Регистрационные данные юридических лиц, филиалов, представительств (Казахстан)")
    short_name = _("Реестр юрлиц (kz)")
    loader_class = DataEgovKzGbdUlLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import DataEgovKzGbdUlModel

        return DataEgovKzGbdUlModel

    @property
    def sitemap(self):
        from .sitemaps import DataEgovKzGbdUlSitemap

        return DataEgovKzGbdUlSitemap

    elastic_model = ElasticDataEgovKzGbdUlModel
    elastic_index = data_egov_kz_gbd_ul_idx
