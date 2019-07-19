from abstract.apps import AbstractConfig
from .loader import ProcurementWinnersLoader
from .elastic_models import ElasticProcurementWinnersModel, procurement_winners_idx


class ProcurementWinnersConfig(AbstractConfig):
    name = "procurement_winners"

    verbose_name = "Переможці в закупівлях"
    short_name = "Закупівлі"
    loader_class = ProcurementWinnersLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import ProcurementWinnersModel

        return ProcurementWinnersModel

    @property
    def sitemap(self):
        from .sitemaps import ProcurementWinnersSitemap

        return ProcurementWinnersSitemap

    elastic_model = ElasticProcurementWinnersModel
    elastic_index = procurement_winners_idx
