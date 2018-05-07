from django.contrib import sitemaps
from .models import Genre, Tag, Studio, Staff


class GenreSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "yearly"

    def items(self):
        return Genre.objects.filter(is_published=True)


class TagSitemap(sitemaps.Sitemap):
    priority = 0.7
    changefreq = "yearly"

    def items(self):
        return Tag.objects.filter(is_published=True)


class StudioSitemap(sitemaps.Sitemap):
    priority = 0.1
    changefreq = "yearly"

    def items(self):
        return Studio.objects.filter(is_published=True)


class StaffSitemap(sitemaps.Sitemap):
    priority = 0.2
    changefreq = "yearly"

    def items(self):
        return Staff.objects.filter(is_published=True)
