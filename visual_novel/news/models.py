from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from core.models import PublishFileModel
from core.fields import ImageFieldWithEnhancedUploadTo


class News(PublishFileModel):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    alias = models.CharField(verbose_name='Алиас (до 30 символов)', max_length=30, default='', blank=True)
    poster = ImageFieldWithEnhancedUploadTo(verbose_name='Постер', null=True, blank=True)
    short_description = models.TextField(verbose_name='Краткое описание', default='', blank=True)
    description = models.TextField(default='', blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(verbose_name='Время создания новости', auto_now_add=True)
    author = models.ForeignKey(User, blank=True, null=True, verbose_name="Автор", on_delete=models.SET_NULL)

    class Meta:
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        file_fields = [
            {
                'field_name': 'poster',
                'path': settings.MEDIA_VN_NEWS
            }
        ]

    def __str__(self):
        return self.title
