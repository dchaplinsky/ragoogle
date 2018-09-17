from django.contrib.sitemaps import Sitemap
from smida_reports.models import SmidaReportModel


class SmidaReportSitemap(Sitemap):
    changefreq = "monthly"
    protocol = "https"
    limit = 50000

    def items(self):
        return SmidaReportModel.objects.order_by("pk")

    def lastmod(self, obj):
        return obj.last_updated_from_dataset
