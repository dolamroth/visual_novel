from django.core.management.base import BaseCommand

from cinfo.models import Genre, Tag, Studio, Staff

from vn_core.utils import YandexMetrica


class Command(BaseCommand):
    def handle(self, *args, **options):
        metrika = YandexMetrica()

        Genre.objects.filter().update(rank_by_visits=None)
        top_genres = metrika.get_genres_by_popularity()
        print(top_genres)
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
