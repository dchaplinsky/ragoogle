from abstract.apps import AbstractConfig
from .loader import GeoinfLicensesLoader
from .elastic_models import ElasticGeoinfLicenseModel, geoinf_licenses_idx


class GeoinfLicensesConfig(AbstractConfig):
    name = "geoinf_licenses"

    verbose_name = "Ліцензії ДП Геоінформ"
    loader_class = GeoinfLicensesLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import GeoinfLicenseModel

        return GeoinfLicenseModel

    @property
    def sitemap(self):
        from .sitemaps import GeoinfLicenseSitemap

        return GeoinfLicenseSitemap

    elastic_model = ElasticGeoinfLicenseModel
    elastic_index = geoinf_licenses_idx
