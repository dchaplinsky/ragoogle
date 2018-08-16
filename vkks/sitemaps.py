from django.contrib.sitemaps import Sitemap
from vkks.models import VKKSModel


class VKKSSitemap(Sitemap):
    changefreq = "monthly"
    protocol = "https"
    limit = 50000

    def items(self):
        return VKKSModel.objects.order_by("pk")

    def lastmod(self, obj):
        return obj.last_updated_from_dataset
