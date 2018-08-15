from django.db import models
from django.urls import reverse

from core.models import PublishModel


class Tag(PublishModel):
    title = models.CharField(verbose_name='название', max_length=256)
    description = models.TextField(verbose_name='описание', max_length=5000, default='', blank=True)
    alias = models.TextField(verbose_name='алиас (до 30 символов)', max_length=30)
    rank_by_visits = models.IntegerField(verbose_name='место по визитам', null=True, blank=True)

    class Meta:
        db_table = 'tags'
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('title', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('chart_index_with_tag', kwargs={'tag_alias': self.alias})
