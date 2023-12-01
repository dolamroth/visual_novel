import datetime

from django.core.management.base import BaseCommand
from django.core.cache import caches

from cinfo.models import Genre, Tag, Studio, Staff
from vn_core.models import VisualNovelStats, VisualNovel

from vn_core.utils import YandexMetrica


cache = caches["default"]


class Command(BaseCommand):
    help = 'Update statistics for first 3 positions by page visits, for chart pages filtered by tags, genres etc.'

    def handle(self, *args, **options):
        Genre.objects.filter().update(rank_by_visits=None)
        Tag.objects.filter().update(rank_by_visits=None)
        Studio.objects.filter().update(rank_by_visits=None)
        Staff.objects.filter().update(rank_by_visits=None)
