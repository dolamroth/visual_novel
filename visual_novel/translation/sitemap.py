from django.contrib import sitemaps
from .models import TranslationItem


class TranslationItemSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return TranslationItem.objects.filter(
            is_published=True,
            visual_novel__is_published=True
        )
