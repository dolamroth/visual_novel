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
        metrika = YandexMetrica()

        Genre.objects.filter().update(rank_by_visits=None)
        top_genres = metrika.get_genres_by_popularity()
        if len(top_genres) >= 3:
            Genre.objects.filter(alias=top_genres[0]).update(rank_by_visits=1)
            Genre.objects.filter(alias=top_genres[1]).update(rank_by_visits=2)
            Genre.objects.filter(alias=top_genres[2]).update(rank_by_visits=3)

        Tag.objects.filter().update(rank_by_visits=None)
        top_tags = metrika.get_tags_by_popularity()
        if len(top_tags) >= 3:
            Tag.objects.filter(alias=top_tags[0]).update(rank_by_visits=1)
            Tag.objects.filter(alias=top_tags[1]).update(rank_by_visits=2)
            Tag.objects.filter(alias=top_tags[2]).update(rank_by_visits=3)

        Studio.objects.filter().update(rank_by_visits=None)
        top_studios = metrika.get_studios_by_popularity()
        if len(top_studios) >= 3:
            Studio.objects.filter(alias=top_studios[0]).update(rank_by_visits=1)
            Studio.objects.filter(alias=top_studios[1]).update(rank_by_visits=2)
            Studio.objects.filter(alias=top_studios[2]).update(rank_by_visits=3)

        Staff.objects.filter().update(rank_by_visits=None)
        top_staff = metrika.get_staff_by_popularity()
        if len(top_staff) >= 3:
            Staff.objects.filter(alias=top_staff[0]).update(rank_by_visits=1)
            Staff.objects.filter(alias=top_staff[1]).update(rank_by_visits=2)
            Staff.objects.filter(alias=top_staff[2]).update(rank_by_visits=3)

        today = datetime.date.today()
        if VisualNovelStats.objects.filter(date=today).exists():
            # Prevent from second run
            if not VisualNovelStats.objects.filter(date=today, rank_by_visits__isnull=False).exists():
                top_visual_novels = metrika.get_novels_by_popularity()
                k = 1
                for alias in top_visual_novels:
                    # metrika.get_novels_by_popularity has inner check that all aliases
                    # correspond to VisualNovel objects in the database
                    visual_novel = VisualNovel.objects.get(alias=alias)

                    try:
                        with cache.lock(f"visual_novel_stats_{visual_novel.alias}_{today}", timeout=10, blocking_timeout=20):
                            today_vn_stats, _ = VisualNovelStats.objects.get_or_create(visual_novel=visual_novel, date=today)

                        today_vn_stats.rank_by_visits = k
                        today_vn_stats.save(update_fields=["rank_by_visits"])
                    except VisualNovelStats.DoesNotExist:
                        pass
                    finally:
                        k += 1
