import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.cache import caches

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
                visual_novels = VisualNovel.objects.filter(vndb_id=vndb_id)

                for visual_novel in visual_novels:
                    with cache.lock(f"visual_novel_stats_{visual_novel.alias}_{today}", timeout=10, blocking_timeout=20):
                        stats, _ = VisualNovelStats.objects.get_or_create(visual_novel=visual_novel, date=today)

                    rating, popularity, vote_count = vndb.update_vn(vndb_id)

                    visual_novel.rate = rating
                    visual_novel.popularity = popularity
                    visual_novel.vote_count = vote_count
                    visual_novel.save(update_fields=["rate", "popularity", "vote_count"])

                    stats.rate = rating
                    stats.popularity = popularity
                    stats.vote_count = vote_count
                    stats.save(update_fields=["rate", "popularity", "vote_count"])
        finally:
            vndb.logout()
