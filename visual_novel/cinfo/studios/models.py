from django.db import models
from core.models import PublishModel


class Studio(PublishModel):
    title = models.CharField(verbose_name='название', max_length=256)
    description = models.TextField(verbose_name='описание', max_length=5000, blank=True, null=True)

    class Meta:
        db_table = 'studios'
        verbose_name = 'Студия'
        verbose_name_plural = 'Студии'

    def __str__(self):
        return self.title
