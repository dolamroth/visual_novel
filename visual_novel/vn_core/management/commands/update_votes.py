import datetime
import random
import anyio
import httpx

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef

from vn_core.models import VisualNovel, VisualNovelStats
from notifications.vk import VK


class Command(BaseCommand):
    def handle(self, *args, **options):
        vk = VK()

        today = datetime.date.today()
        sq = VisualNovelStats.objects.filter(visual_novel_id=OuterRef("id"), date=today).values_list("id")
        all_visual_novels = VisualNovel.objects.filter(~Exists(sq)).values_list('vndb_id', flat=True)

        all_visual_novels_ids = list(set(all_visual_novels))
        random.shuffle(all_visual_novels_ids)
        to_collect_ids = set()

        for vndb_id in set(all_visual_novels_ids):
            for visual_novel in VisualNovel.objects.filter(vndb_id=vndb_id):
                try:
                    stats = VisualNovelStats.objects.get(visual_novel=visual_novel, date=today)
                except VisualNovelStats.DoesNotExist:
                    to_collect_ids.add(visual_novel.vndb_id)
                except VisualNovelStats.MultipleObjectsReturned:
                    stats = VisualNovelStats.objects.filter(visual_novel=visual_novel, date=today)
                    first_id = stats.first().id
                    stats.exclude(id=first_id).delete()

        try:
            results = anyio.run(self.async_handle, to_collect_ids)
        except:
            vk.send_to_user(msg='Проблема с подключением к VNDb', user_id=settings.VK_ADMIN_LOGIN)
            return

        for vndb_id in results.keys():
            visual_novel = VisualNovel.objects.filter(vndb_id=vndb_id).first()
            if not visual_novel:
                continue

            rating, vote_count = results[vndb_id]

            stats, created = VisualNovelStats.objects.get_or_create(visual_novel=visual_novel, date=today)

            visual_novel.rate = rating
            visual_novel.popularity = 0
            visual_novel.vote_count = vote_count
            visual_novel.save(update_fields=["rate", "popularity", "vote_count"])

            stats.rate = rating
            stats.popularity = 0
            stats.vote_count = vote_count
            stats.save(update_fields=["rate", "popularity", "vote_count"])

    async def async_handle(self, vndb_id_set):
        result = {}

        with anyio.fail_after(2700):
            for vndb_id in vndb_id_set:
                async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=30, connect=30)) as client:
                    response = await client.post("https://api.vndb.org/kana/vn", json={
                        "filters": ["id", "=", f"v{vndb_id}"],
                        "fields": "rating, votecount",
                    })
                    vn_obj = response.json()
                    rating = round(float(vn_obj['results'][0]['rating']) * 10.0)
                    vote_count = round(vn_obj['results'][0]['votecount'])
                    result[vndb_id] = (rating, vote_count)

                await anyio.sleep(5)

        return result
