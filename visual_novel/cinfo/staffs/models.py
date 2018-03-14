from django.db import models
from core.models import PublishModel


class Staff(PublishModel):
    title = models.CharField(verbose_name='название', max_length=256)
    description = models.TextField(verbose_name='описание', max_length=5000, blank=True, null=True)
    alias = models.TextField(verbose_name='алиас (до 30 символов)', max_length=30, default='')

    class Meta:
        db_table = 'staffs'
        verbose_name = 'Персоналия'
        verbose_name_plural = 'Персоналии'

    def __str__(self):
        return self.title
