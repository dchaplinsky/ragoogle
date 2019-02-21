from abstract.apps import AbstractConfig
from .loader import SmidaReportLoader
from .elastic_models import ElasticSmidaReportModel, smida_report_idx


class SmidaReportConfig(AbstractConfig):
    name = "smida_reports"
    verbose_name = "Звіти акціонерних товариств СМІДА"
    short_name = "СМІДА"
    loader_class = SmidaReportLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import SmidaReportModel
        return SmidaReportModel
    
    @property
    def sitemap(self):
        from .sitemaps import SmidaReportSitemap

        return SmidaReportSitemap

    elastic_model = ElasticSmidaReportModel
    elastic_index = smida_report_idx