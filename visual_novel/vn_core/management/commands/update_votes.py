import datetime
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef

from vn_core.models import VisualNovel, VisualNovelStats
from vn_core.utils import VndbStats
from notifications.vk import VK


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
            today = datetime.date.today()
            sq = VisualNovelStats.objects.filter(visual_novel_id=OuterRef("id"), date=today).values_list("id")
            all_visual_novels = VisualNovel.objects.filter(~Exists(sq)).values_list('vndb_id', flat=True)

            for vndb_id in set(all_visual_novels):
                for visual_novel in VisualNovel.objects.filter(vndb_id=vndb_id):
                    try:
                        stats = VisualNovelStats.objects.get(visual_novel=visual_novel, date=today)
                    except:
                        rating, popularity, vote_count = vndb.update_vn(vndb_id)

                        stats, created = VisualNovelStats.objects.get_or_create(visual_novel=visual_novel, date=today)

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
