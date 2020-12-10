from abstract.apps import AbstractConfig
from .loader import RegistryAndozTjLoader
from .elastic_models import ElasticRegistryAndozTjModel, registry_andoz_tj_idx
from django.utils.translation import gettext_lazy as _


class RegistryAndozTjConfig(AbstractConfig):
    name = "registry_andoz_tj"

    verbose_name = _("Реестр компаний (Таджикистан)")
    short_name = _("Реестр компаний (tj)")

    loader_class = RegistryAndozTjLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import RegistryAndozTjModel

        return RegistryAndozTjModel

    @property
    def sitemap(self):
        from .sitemaps import RegistryAndozTjSitemap

        return RegistryAndozTjSitemap

    elastic_model = ElasticRegistryAndozTjModel
    elastic_index = registry_andoz_tj_idx
