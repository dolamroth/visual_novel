from django.db import models
from django.urls import reverse

from core.models import PublishModel


class Translator(PublishModel):
    title = models.CharField(verbose_name='Переводчик', max_length=256)
    description = models.TextField(verbose_name='описание', max_length=5000, blank=True, default='')
    alias = models.TextField(verbose_name='алиас (до 30 символов)', max_length=30)
    url = models.CharField(max_length=200, verbose_name="базовая ссылка", null=True, blank=True)

    class Meta:
        db_table = 'translator_teams'
        verbose_name = 'Переводчик'
        verbose_name_plural = 'Переводчики'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('chart_index_with_translator', kwargs={'translator_alias': self.alias})
