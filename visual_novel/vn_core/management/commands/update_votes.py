import datetime

from django.core.management.base import BaseCommand

from vn_core.models import VisualNovel, VisualNovelStats
from vn_core.utils import VndbStats


class Command(BaseCommand):
    def handle(self, *args, **options):
        vndb = VndbStats()
        vndb.login()
        if not vndb.connected:
            print(vndb.status)
            return

        try:
            all_visual_novels = VisualNovel.objects.all().values_list('vndb_id', flat=True)
            today = datetime.date.today()
            for vndb_id in all_visual_novels:
                vn = VisualNovel.objects.get(vndb_id=vndb_id)
                try:
                    VisualNovelStats.objects.get(visual_novel=vn, data=today)
                except VisualNovelStats.DoesNotExist:
                    stats = VisualNovelStats.objects.create(visual_novel=vn)
                    rating, popularity, vote_count = vndb.update_vn(vndb_id)

                    vn.rate=rating
                    vn.popularity=popularity
                    vn.vote_count=vote_count
                    vn.save()

                    stats.rate = rating
                    stats.popularity = popularity
                    stats.vote_count = vote_count
                    stats.save()
        finally:
            vndb.logout()
        pass
