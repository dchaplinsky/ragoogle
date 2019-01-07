from django.contrib.sitemaps import Sitemap
from dabi_licenses.models import DabiLicenseModel


class DabiLicenseSitemap(Sitemap):
    changefreq = "monthly"
    protocol = "https"
    limit = 50000

    def items(self):
        return DabiLicenseModel.objects.only("id", "last_updated_from_dataset").order_by("pk")

    def lastmod(self, obj):
        return obj.last_updated_from_dataset
