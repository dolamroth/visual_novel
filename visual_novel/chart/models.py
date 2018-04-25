from django.db import models

from core.models import PublishModel
from vn_core.models import VisualNovel, VNScreenshot


class ChartItem(PublishModel):
    visual_novel = models.ForeignKey(VisualNovel, on_delete=models.PROTECT)
    date_of_translation = models.DateField(verbose_name='дата перевода на русский (первого)')
    comment = models.TextField(verbose_name='комментарий', max_length=5000, default='', blank=True)

    class Meta:
        db_table = 'chart_items'
        verbose_name = 'Итем чарта'
        verbose_name_plural = 'Итемы чарта'

    def __str__(self):
        return self.visual_novel.title


class ChartItemScreenshot(VNScreenshot):
    item = models.ForeignKey(ChartItem, on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='порядок', default=0)

    class Meta:
        db_table = 'chart_item_to_screenshot'
        verbose_name = 'Скриншот'
        verbose_name_plural = 'Скриншоты'

    def __str__(self):
        return 'Скриншот для {}'.format(self.item.visual_novel.title)
