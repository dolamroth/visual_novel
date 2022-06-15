from django.db import models
from django.urls import reverse

from cinfo.translation_languages.models import TranslationLanguage
from cinfo.translators.models import Translator
from core.models import PublishModel
from vn_core.models import VisualNovel, VNScreenshot


class ChartItem(PublishModel):
    visual_novel = models.ForeignKey(VisualNovel, on_delete=models.PROTECT, verbose_name='Визуальная новелла')
    date_of_translation = models.DateField(verbose_name='дата перевода на русский (первого)')
    comment = models.TextField(verbose_name='комментарий', max_length=5000, default='', blank=True)
    translations = models.ManyToManyField(Translator, through='ChartItemTranslator',
                                          blank=True, verbose_name='Переводы')

    class Meta:
        db_table = 'chart_items'
        verbose_name = 'Итем чарта'
        verbose_name_plural = 'Итемы чарта'
        ordering = ('visual_novel__title', )

    def __str__(self):
        return self.visual_novel.title

    def get_absolute_url(self):
        return reverse('detail_chart', kwargs={'vn_alias': self.visual_novel.alias})


class ChartItemScreenshot(VNScreenshot):
    item = models.ForeignKey(ChartItem, on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='порядок', default=0)

    class Meta(VNScreenshot.Meta):
        db_table = 'chart_item_to_screenshot'
        verbose_name = 'Скриншот'
        verbose_name_plural = 'Скриншоты'

    def __str__(self):
        return 'Скриншот для {}'.format(self.item.visual_novel.title)


class ChartItemTranslator(models.Model):
    item = models.ForeignKey(ChartItem, on_delete=models.CASCADE, verbose_name='Визуальная новелла')
    translator = models.ForeignKey(Translator, on_delete=models.PROTECT, verbose_name='Переводчик',
                                   null=False, blank=False)
    language = models.ForeignKey(TranslationLanguage, on_delete=models.PROTECT, verbose_name='Язык перевода',
                                 null=False, blank=False)

    class Meta:
        db_table = 'chart_item_to_translators'
        verbose_name = 'Перевод новеллы'
        verbose_name_plural = 'Переводы новелл'

    def __str__(self):
        return f'Перевод {self.item.visual_novel.title} командой {self.translator.title}'
