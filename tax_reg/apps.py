from abstract.apps import AbstractConfig
from .loader import TaxRegLoader
from .elastic_models import ElasticTaxRegModel, tax_reg_idx


class TaxRegConfig(AbstractConfig):
    name = "tax_reg"

    verbose_name = "Реєстрація компаній в ДФС"
    short_name = "ДФС"
    loader_class = TaxRegLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import TaxRegModel

        return TaxRegModel

    @property
    def sitemap(self):
        from .sitemaps import TaxRegSitemap

        return TaxRegSitemap

    elastic_model = ElasticTaxRegModel
    elastic_index = tax_reg_idx
