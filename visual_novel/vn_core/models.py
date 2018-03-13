import os

from django.db import models

from core.models import PublishModel
from cinfo.models import Longevity

def posters_directory_path(instance, filename):
    return os.path.join('vn_poster', filename)


class VisualNovel(PublishModel):
    title = models.CharField(verbose_name='название', max_length=256)
    alternative_title = models.CharField(verbose_name='альтернативные названия', max_length=500, default='')
    description = models.TextField(verbose_name='описание', max_length=8000, default='')
    photo = models.ImageField(verbose_name='фотография', upload_to=posters_directory_path,
                              null=False, blank=False)
    date_of_release = models.DateField(verbose_name='дата релиза')
    vndb_id = models.IntegerField(verbose_name='id на VNDb')
    steam_link = models.CharField(verbose_name='ссылка в Steam', max_length=400, null=True, blank=True)
    longevity = models.ForeignKey(Longevity, verbose_name='продолжительность', on_delete=models.PROTECT,
                                  null=True, blank=True)

    class Meta:
        db_table = 'vncore'
        verbose_name = 'Визуальная новелла'
        verbose_name_plural = 'Визуальные новеллы'

    def __str__(self):
        return self.title
