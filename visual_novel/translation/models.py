from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from core.models import PublishModel
from vn_core.models import VisualNovel


class TranslationStatistics(models.Model):
    tree_id = models.IntegerField(default=0)
    pictures_statistics = models.TextField(verbose_name='Статистика изображений', max_length=500, default='')
    technical_statistics = models.TextField(verbose_name='Статистика тех. части', max_length=500, default='')
    comment = models.TextField(verbose_name='Статистика изображений', max_length=2000, default='')
    last_update = models.DateTimeField(verbose_name='Дата последнего обновления',
                                       auto_now_add=True, null=True, blank=True)
    total_rows = models.IntegerField(default=0, verbose_name='Всего строк')
    translated = models.IntegerField(default=0, verbose_name='Переведено')
    edited_first_pass = models.IntegerField(default=0, verbose_name='Первый проход редактуры')
    edited_second_pass = models.IntegerField(default=0, verbose_name='Второй проход редактуры')

    class Meta:
        db_table = 'statistics_item'

    def __str__(self):
        return 'Статистика перевода {}'.format(self.tree_id)


class TranslationStatisticsChapter(MPTTModel):
    title = models.CharField(max_length=50, default='')
    script_title = models.CharField(max_length=50, default='')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',
                            db_index=True, on_delete=models.CASCADE)
    is_chapter = models.BooleanField(default=False)
    total_rows = models.IntegerField(default=0)
    translated = models.IntegerField(default=0)
    edited_first_pass = models.IntegerField(default=0)
    edited_second_pass = models.IntegerField(default=0)
    last_update = models.DateTimeField(verbose_name='Дата последнего обновления',
                                       auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'statistics_chapter'

    def __str__(self):
        return self.script_title

    def statistics_name(self):
        name = self.script_title
        if self.is_chapter:
            name = '<strong>' + name + '</strong>'
        name = '<span style="margin-left:{}em">{}</span>'.format(self.get_level(), name)
        return name

    def select_like_statistics_name(self, base_level = 0):
        return '---' * (self.get_level() - base_level) + ' ' + str(self.script_title)

    def delete(self):
        super(TranslationStatisticsChapter, self).delete()


class TranslationBetaLink(PublishModel):
    title = models.CharField(max_length=50, default='')
    url = models.CharField(max_length=200, default='')
    comment = models.TextField(max_length=2000, default='')
    translation_item = models.ForeignKey('TranslationItem', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        db_table = 'statistics_betalink'

    def __str__(self):
        return self.url

    def delete(self, force=False):
        if force:
            super(TranslationBetaLink, self).delete()
        else:
            self.is_published = False
            super(TranslationBetaLink, self).save()


class TranslationItem(PublishModel):
    visual_novel = models.ForeignKey(VisualNovel, on_delete=models.PROTECT, verbose_name='Визуальная новелла')
    statistics = models.ForeignKey(TranslationStatistics, on_delete=models.SET_NULL,
                                   null=True, blank=True, verbose_name='Привязанная статистика')

    class Meta:
        db_table = 'translation_items'
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'

    def __str__(self):
        return 'Перевод {}'.format(self.visual_novel.title)

    def save(self, *args, **kwargs):
        if not self.id:
            parental_translation_node, _ = TranslationStatisticsChapter.objects.get_or_create(
                parent=None,
                title='Раздел самого высокого уровня',
                script_title='Раздел самого высокого уровня',
                is_chapter=True
            )
            translation_statistics, _ = TranslationStatistics.objects.get_or_create(
                tree_id=parental_translation_node.tree_id
            )
            self.statistics = translation_statistics
        super(TranslationItem, self).save(*args, **kwargs)

    def delete(self):
        tree_id = self.statistics.tree_id
        TranslationStatisticsChapter.objects.filter(tree_id=tree_id).delete()
        TranslationStatistics.objects.get(pk=self.statistics.pk).delete()
        super(TranslationItem, self).delete()
