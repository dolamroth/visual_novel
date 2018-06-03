import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

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
            for stats in VisualNovelStats.objects.filter(date=today):
                vndb_id = stats.visual_novel.vndb_id
                rating, popularity, vote_count = vndb.update_vn(vndb_id)
                vn = VisualNovel.objects.get(id=stats.visual_novel.id)
                vn.rate = rating
                vn.popularity = popularity
                vn.vote_count = vote_count
                vn.save()

                stats.rate = rating
                stats.popularity = popularity
                stats.vote_count = vote_count
                stats.save()
        finally:
            vndb.logout()
        pass
