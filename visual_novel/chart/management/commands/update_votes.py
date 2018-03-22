from django.core.management.base import BaseCommand

from vn_core.models import VisualNovel
from vn_core.utils import vndb_socket_login, vndb_socket_logout, vndb_socket_update_vn


class Command(BaseCommand):
    def handle(self, *args, **options):

        sock = vndb_socket_login()
        if sock is None:
            return

        try:
            all_visual_novels = VisualNovel.objects.filter(is_published=True).values_list('vndb_id', flat=True)
            for vndb_id in all_visual_novels:
                rating, popularity, vote_count = vndb_socket_update_vn(sock, vndb_id)
                print(vndb_id, rating, popularity, vote_count)
                VisualNovel.objects.filter(vndb_id=vndb_id).update(
                    rate=rating,
                    popularity=popularity,
                    vote_count=vote_count
                )
        finally:
            vndb_socket_logout(sock)
        pass
