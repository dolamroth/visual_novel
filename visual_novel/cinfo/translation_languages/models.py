from django.db import models

from core.models import PublishModel


class TranslationLanguage(PublishModel):
    title = models.CharField(verbose_name='Направление перевода (в свободной форме)', max_length=256)

    class Meta:
        db_table = 'translation_languages'
        verbose_name = 'Направление перевода'
        verbose_name_plural = 'Направления перевода'

    def __str__(self):
        return self.title
