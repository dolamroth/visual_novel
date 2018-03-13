from django.db import models

from core.models import PublishModel
from vn_core.models import VisualNovel


class ChartItem(PublishModel):
    visual_novel = models.ForeignKey(VisualNovel, on_delete=models.PROTECT)
    date_of_translation = models.DateField(verbose_name='дата перевода на русский (первого)')

    class Meta:
        db_table = 'chart_items'
        verbose_name = 'Итем чарта'
        verbose_name_plural = 'Итемы чарта'

    def __str__(self):
        return self.visual_novel.title
