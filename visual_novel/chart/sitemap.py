from django.contrib import sitemaps
from .models import ChartItem


class ChartItemSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = "monthly"

    def items(self):
        return ChartItem.objects.filter(
            is_published=True,
            visual_novel__is_published=True
        )
