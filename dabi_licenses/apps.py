from django.apps import AppConfig
from .loader import DabiLicensesLoader
from .elastic_models import ElasticDabiLicenseModel, dabi_licenses_idx


class DabiLicensesConfig(AppConfig):
    name = "dabi_licenses"

    verbose_name = "Ліцензії ДАБІ"
    loader_class = DabiLicensesLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import DabiLicenseModel

        return DabiLicenseModel

    @property
    def sitemap(self):
        from .sitemaps import DabiLicenseSitemap

        return DabiLicenseSitemap

    elastic_model = ElasticDabiLicenseModel
    elastic_index = dabi_licenses_idx
