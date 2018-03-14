from django.db import models
from core.models import PublishModel


class Tag(PublishModel):
    title = models.CharField(verbose_name='название', max_length=256)
    description = models.TextField(verbose_name='описание', max_length=5000, default='')
    alias = models.TextField(verbose_name='алиас (до 30 символов)', max_length=30, default='')

    class Meta:
        db_table = 'tags'
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.title
