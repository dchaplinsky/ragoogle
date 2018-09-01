from django.contrib.sitemaps import Sitemap
from cvk_2015.models import CVK2015Model


class CVK2015Sitemap(Sitemap):
    changefreq = "monthly"
    protocol = "https"
    limit = 50000

    def items(self):
        return CVK2015Model.objects.order_by("pk")
