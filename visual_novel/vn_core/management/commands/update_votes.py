import datetime
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef

from vn_core.models import VisualNovel, VisualNovelStats
from vn_core.utils import VndbStats
from notifications.vk import VK


cache = caches["default"]


class Command(BaseCommand):
    def handle(self, *args, **options):
        vndb = VndbStats()
        try:
            vndb.login()
        except VndbStats.VndbAuthError:
            vk = VK()
            vk.send_to_user(
                msg='Проблема с подключением к VNDb',
                user_id=settings.VK_ADMIN_LOGIN
            )
            return

        try:
            seen_vndb_id = set()
            all_visual_novels = VisualNovel.objects.all().values_list('vndb_id', flat=True)
            today = datetime.date.today()

            for vndb_id in all_visual_novels:
                if vndb_id in seen_vndb_id:
                    continue

                seen_vndb_id.add(vndb_id)
                today = datetime.date.today()
                sq = VisualNovelStats.objects.filter(visual_novel_id=OuterRef("id"), date=today).values_list("id")
                all_visual_novels = VisualNovel.objects.filter(~Exists(sq)).values_list('vndb_id', flat=True)

                for visual_novel in visual_novels:
                    stats, created = VisualNovelStats.objects.get_or_create(visual_novel=visual_novel, date=today)

                    if created:
                        continue

                    rating, popularity, vote_count = vndb.update_vn(vndb_id)

                    visual_novel.rate = rating
                    visual_novel.popularity = popularity
                    visual_novel.vote_count = vote_count
                    visual_novel.save(update_fields=["rate", "popularity", "vote_count"])

                    stats.rate = rating
                    stats.popularity = popularity
                    stats.vote_count = vote_count
                    stats.save(update_fields=["rate", "popularity", "vote_count"])
                    time.sleep(5)
        finally:
            vndb.logout()
