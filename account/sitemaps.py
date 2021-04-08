from django.contrib import sitemaps
from django.urls import reverse
#网站地图sitemap

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['login']

    def location(self, item):
        return reverse(item)
