from abstract.apps import AbstractConfig
from .loader import TaxDebtsLoader
from .elastic_models import ElasticTaxDebtsModel, tax_debts_idx


class TaxDebtsConfig(AbstractConfig):
    name = "tax_debts"

    verbose_name = "Податковий борг"
    short_name = "Борг"
    loader_class = TaxDebtsLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import TaxDebtsModel

        return TaxDebtsModel

    @property
    def sitemap(self):
        from .sitemaps import TaxDebtsSitemap

        return TaxDebtsSitemap

    elastic_model = ElasticTaxDebtsModel
    elastic_index = tax_debts_idx
