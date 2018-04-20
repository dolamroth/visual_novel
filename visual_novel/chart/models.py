from django.db import models
from django.utils.html import format_html

from core.models import PublishModel
from vn_core.models import VisualNovel, VNScreenshot


class ChartItem(PublishModel):
    visual_novel = models.ForeignKey(VisualNovel, on_delete=models.PROTECT)
    date_of_translation = models.DateField(verbose_name='дата перевода на русский (первого)')
    comment = models.TextField(verbose_name='комментарий', max_length=5000, default='')

    class Meta:
        db_table = 'chart_items'
        verbose_name = 'Итем чарта'
        verbose_name_plural = 'Итемы чарта'

    def __str__(self):
        return self.visual_novel.title


class ChartItemScreenshot(VNScreenshot):
    item = models.ForeignKey(ChartItem, on_delete=models.PROTECT)
    order = models.IntegerField(verbose_name='порядок', default=0)

    class Meta:
        db_table = 'chart_item_to_screenshot'

    def __str__(self):
        if self.title:
            return self.title
        return 'Скриншот для {}'.format(self.item.visual_novel.title)

    def image_tag(self):
        return format_html('<img src="%s" width=200 height=150 />' % self.image.url if self.image else '')

    image_tag.short_description = 'Фотография'
    image_tag.allow_tags = True

