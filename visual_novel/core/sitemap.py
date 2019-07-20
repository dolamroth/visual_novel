from django.contrib import sitemaps
from django.urls import reverse


class StaticViewsSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = "daily"

    def items(self):
        return ['main', 'about', 'chart_index', 'translations_all', 'news_list', ]

    def location(self, item):
        return reverse(item)
