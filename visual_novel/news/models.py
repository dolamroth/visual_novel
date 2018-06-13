from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from sanitizer.models import SanitizedTextField

from core.models import PublishFileModel
from core.fields import ImageFieldWithEnhancedUploadTo


class News(PublishFileModel):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    alias = models.CharField(verbose_name='Алиас (до 30 символов)', max_length=30, default='', blank=True)
    poster = ImageFieldWithEnhancedUploadTo(verbose_name='Постер', null=True, blank=True)
    short_description = SanitizedTextField(verbose_name='Краткое описание', max_length=512, default='', blank=True,
        strip=False, allowed_attributes=['href', 'src', 'style', 'title'],
        allowed_tags=['a', 'p', 'img', 'table', 'tr', 'td', 'th', 'tbody', 'thead', 'span', 'div', 'br', 'b', 'i'])
    description = SanitizedTextField(max_length=6000,
        allowed_tags=['a', 'p', 'img', 'table', 'tr', 'td', 'th', 'tbody', 'thead', 'span', 'div', 'br', 'b', 'i'],
        allowed_attributes=['href', 'src', 'style', 'title'],
        default='', blank=True, strip=False, verbose_name='Описание')
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


News._meta.get_field('short_description').help_text = "Допустимо использовать html-теги {} и парамеры {}".format(
        ', '.join(['<b>' + d + '</b>' for d in News._meta.get_field('short_description')._sanitizer_allowed_tags]),
        ', '.join(['<b>' + d + '</b>' for d in News._meta.get_field('short_description')._sanitizer_allowed_attributes])
    )

News._meta.get_field('description').help_text = "Допустимо использовать html-теги {} и парамеры {}".format(
        ', '.join(['<b>' + d + '</b>' for d in News._meta.get_field('description')._sanitizer_allowed_tags]),
        ', '.join(['<b>' + d + '</b>' for d in News._meta.get_field('description')._sanitizer_allowed_attributes])
    )

