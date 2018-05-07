from django.db import models

from core.models import PublishModel


class Longevity(PublishModel):

    title = models.CharField(verbose_name='название', max_length=100)
    min_length = models.IntegerField(verbose_name='минимальная продолжительность', null=True, blank=True)
    max_length = models.IntegerField(verbose_name='максимальная продолжительность', null=True, blank=True)
    alias = models.TextField(verbose_name='алиас (до 30 символов)', max_length=30)

    class Meta:
        db_table = 'longevity'
        verbose_name = 'Продолжительность'
        verbose_name_plural = 'Продолжительности'

    def __str__(self):
        explanation = ''
        if not self.min_length:
            explanation = '(менее {} часов)'.format(self.max_length)
        elif not self.max_length:
            explanation = '(более {} часов)'.format(self.min_length)
        else:
            explanation = '(от {} до {} часов)'.format(self.min_length, self.max_length)
        return self.title + ' ' + explanation
