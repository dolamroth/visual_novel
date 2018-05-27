import datetime

from django.core.management.base import BaseCommand

from vn_core.models import VisualNovel, VisualNovelStats
from vn_core.utils import vndb_socket_login, vndb_socket_logout, vndb_socket_update_vn


class Command(BaseCommand):
    def handle(self, *args, **options):

        sock = vndb_socket_login()
        if sock is None:
            print('Vndb connection error')
            return

        try:
            all_visual_novels = VisualNovel.objects.all().values_list('vndb_id', flat=True)
            now_date = datetime.datetime.utcnow().date()
            for vndb_id in all_visual_novels:
                rating, popularity, vote_count = vndb_socket_update_vn(sock, vndb_id)
                print(vndb_id, rating, popularity, vote_count)
                vn = VisualNovel.objects.filter(vndb_id=vndb_id)
                vn.update(
                    rate=rating,
                    popularity=popularity,
                    vote_count=vote_count
                )
                try:
                    VisualNovelStats.objects.get(visual_novel=vn, data=now_date)
                except VisualNovelStats.DoesNotExist:
                    VisualNovelStats.objects.create(visual_novel=vn, rate=rating, popularity=popularity,
                                                    vote_count=vote_count)
        finally:
            vndb_socket_logout(sock)
        pass
