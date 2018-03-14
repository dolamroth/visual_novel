from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from core.models import PublishModel
from vn_core.models import VisualNovel


class TranslationItem(PublishModel):
    visual_novel = models.ForeignKey(VisualNovel, on_delete=models.PROTECT)
    statistics = models.ForeignKey('TranslationStatistics', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        db_table = 'translation_items'
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'

    def __str__(self):
        return self.visual_novel.title


class TranslationStatistics(models.Model):
    tree_id = models.IntegerField(default=0)
    pictures_statistics = models.TextField(verbose_name='Статистика изображений', max_length=500, default='')
    technical_statistics = models.TextField(verbose_name='Статистика тех. части', max_length=500, default='')
    comment = models.TextField(verbose_name='Статистика изображений', max_length=2000, default='')

    class Meta:
        db_table = 'statistics_item'

    def __str__(self):
        return 'Статистика перевода {}'.format(self.tree_id)


class TranslationStatisticsChapter(MPTTModel):
    title = models.CharField(max_length=50, default='')
    script_title = models.CharField(max_length=50, default='')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',
                            db_index=True, on_delete=models.PROTECT)
    is_chapter = models.BooleanField(default=False)
    total_rows = models.IntegerField(default=0)
    translated = models.IntegerField(default=0)
    edited_first_pass = models.IntegerField(default=0)
    edited_second_pass = models.IntegerField(default=0)

    class Meta:
        db_table = 'statistics_chapter'

    def __str__(self):
        return self.script_title
