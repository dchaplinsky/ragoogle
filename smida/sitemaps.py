from django.contrib.sitemaps import Sitemap
from smida.models import SmidaModel


class SMIDASitemap(Sitemap):
    changefreq = "monthly"
    protocol = "https"
    limit = 50000

    def items(self):
        return SmidaModel.objects.order_by("pk")

    def lastmod(self, obj):
        return obj.last_updated_from_dataset
