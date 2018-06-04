from django.db import models
from django.urls import reverse

from core.models import PublishModel


class Genre(PublishModel):
    title = models.CharField(verbose_name='название', max_length=256)
    description = models.TextField(verbose_name='описание', max_length=5000, blank=True, default='')
    alias = models.TextField(verbose_name='алиас (до 30 символов)', max_length=30)

    class Meta:
        db_table = 'genres'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('title', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('chart_index_with_genre', kwargs={'genre_alias': self.alias})
