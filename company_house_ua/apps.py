from abstract.apps import AbstractConfig
from .loader import CompanyHouseUaLoader
from .elastic_models import ElasticCompanyHouseUaModel, company_house_ua_idx


class CompanyHouseUaConfig(AbstractConfig):
    name = "company_house_ua"

    verbose_name = "Британський реєстр компаній"
    short_name = "Світ"
    loader_class = CompanyHouseUaLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import CompanyHouseUaModel

        return CompanyHouseUaModel

    @property
    def sitemap(self):
        from .sitemaps import CompanyHouseUaSitemap

        return CompanyHouseUaSitemap

    elastic_model = ElasticCompanyHouseUaModel
    elastic_index = company_house_ua_idx
