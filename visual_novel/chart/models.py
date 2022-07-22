from django.db import models
from django.urls import reverse

from cinfo.translation_languages.models import TranslationLanguage
from cinfo.translators.models import Translator
from core.models import PublishModel
from vn_core.models import VisualNovel, VNScreenshot
from django.contrib.auth.models import User


class ChartItem(PublishModel):
    visual_novel = models.ForeignKey(VisualNovel, on_delete=models.PROTECT, verbose_name='Визуальная новелла')
    date_of_translation = models.DateField(verbose_name='дата перевода на русский (первого)')
    comment = models.TextField(verbose_name='комментарий', max_length=5000, default='', blank=True)
    translations = models.ManyToManyField(Translator, through='ChartItemTranslator', blank=True, verbose_name='Переводы')
    favorites = models.ManyToManyField(User, through='ChartItemToUser', related_name='chart_favorites')
    rating = models.ManyToManyField(User, through='ChartRating', related_name='chart_rating')

    class Meta:
        db_table = 'chart_items'
        verbose_name = 'Итем чарта'
        verbose_name_plural = 'Итемы чарта'
        ordering = ('visual_novel__title', )

    def __str__(self):
        return self.visual_novel.title

    def get_absolute_url(self):
        return reverse('detail_chart', kwargs={'vn_alias': self.visual_novel.alias})

    def get_average_rating(self) -> float:
        all_rated = self.rating.values_list('chart_rating')
        if not all_rated:
            return 0

        return round(sum([rating[0] for rating in all_rated]) / len(all_rated), 2)


class ChartItemScreenshot(VNScreenshot):
    item = models.ForeignKey(ChartItem, on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='порядок', default=0)

    class Meta(VNScreenshot.Meta):
        db_table = 'chart_item_to_screenshot'
        verbose_name = 'Скриншот'
        verbose_name_plural = 'Скриншоты'

    def __str__(self):
        return f'Скриншот для {self.item.visual_novel.title}'


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


class ChartItemToUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    chart_item = models.ForeignKey(ChartItem, on_delete=models.CASCADE, verbose_name='Итем чарта')

    class Meta:
        verbose_name = 'Избранные новеллы'
        verbose_name_plural = 'Избранные новеллы'
        constraints = [
            models.UniqueConstraint(fields=['user', 'chart_item'], name='favorite')
        ]

    def __str__(self):
        return f'{self.user.id} - {self.chart_item.visual_novel.title}'


class ChartRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    chart_item = models.ForeignKey(ChartItem, on_delete=models.CASCADE, verbose_name='Итем чарта')
    rating = models.PositiveIntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = 'Рейтинг новеллы'
        verbose_name_plural = 'Рейтинг новеллы'
        constraints = [
            models.UniqueConstraint(fields=['user', 'chart_item'], name='rating')
        ]

    def __str__(self):
        return f'{self.user.id} - {self.chart_item.visual_novel.title} | {self.rating}'

