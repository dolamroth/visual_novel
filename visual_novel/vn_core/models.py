import os
from PIL import Image

from django.conf import settings
from django.db import models

from core.models import PublishModel, PublishFileModel
from core.fields import ImageFieldWithEnhancedUploadTo
from cinfo.models import Longevity, Genre, Tag, Studio, Staff, StaffRole

from .utils import vndb_socket_login, vndb_socket_logout, vndb_socket_update_vn


class VisualNovel(PublishFileModel):
    title = models.CharField(verbose_name='название', max_length=256)
    alternative_title = models.CharField(verbose_name='альтернативные названия', max_length=500, default='')
    description = models.TextField(verbose_name='описание', max_length=8000, default='')
    photo = ImageFieldWithEnhancedUploadTo(verbose_name='фотография', null=True, blank=True)
    date_of_release = models.DateField(verbose_name='дата релиза')
    vndb_id = models.IntegerField(verbose_name='id на VNDb')
    steam_link = models.CharField(verbose_name='ссылка в Steam', max_length=400, null=True, blank=True)
    longevity = models.ForeignKey(Longevity, verbose_name='продолжительность', on_delete=models.PROTECT,
                                  null=True, blank=True)
    genres = models.ManyToManyField(Genre, through='VNGenre', verbose_name='жанры', blank=True)
    tags = models.ManyToManyField(Tag, through='VNTag', verbose_name='тэги', blank=True)
    studios = models.ManyToManyField(Studio, through='VNStudio', verbose_name='студии', blank=True)
    staff = models.ManyToManyField(Staff, through='VNStaff', verbose_name='создатели', blank=True)
    alias = models.TextField(verbose_name='алиас (до 30 символов)', max_length=30, default='')
    rate = models.IntegerField(verbose_name='оценка на VNDb', default=0)
    popularity = models.IntegerField(verbose_name='популярность на VNDb', default=0)
    vote_count = models.IntegerField(verbose_name='число голосов на VNDb', default=0)

    class Meta:
        db_table = 'vncore'
        verbose_name = 'Визуальная новелла'
        verbose_name_plural = 'Визуальные новеллы'
        file_fields = [
            {
                'field_name': 'photo',
                'path': settings.MEDIA_VN_POSTER_DIRECTORY
            }
        ]

    def __str__(self):
        return self.title

    def get_rate(self):
        return "{0:.2f}".format(self.rate / 100.0)

    def get_popularity(self):
        return "{0:.2f}".format(self.popularity / 100.0)

    def additional_action_on_save(self, list_of_changed_fields, created):
        vndb_id = self.vndb_id
        if created and (type(vndb_id) == int):
            sock = None
            try:
                sock = vndb_socket_login()
                rate, popularity, vote_count = vndb_socket_update_vn(sock, vndb_id)
                self.rate = rate
                self.popularity = popularity
                self.vote_count = vote_count
                VisualNovelStats.objects.create(rate=rate, popularity=popularity, vote_count=vote_count)
            finally:
                vndb_socket_logout(sock)


class VisualNovelStats(models.Model):
    visual_novel = models.ForeignKey(VisualNovel, on_delete=models.PROTECT)
    data = models.DateField(auto_now_add=True, verbose_name='Дата')
    rate = models.IntegerField(verbose_name='оценка на VNDb', default=0)
    popularity = models.IntegerField(verbose_name='популярность на VNDb', default=0)
    vote_count = models.IntegerField(verbose_name='число голосов на VNDb', default=0)

    class Meta:
        db_table = 'vnstats'
        verbose_name = 'Оценка визуальной новеллы'
        verbose_name_plural = 'Оценки визуальных новелл'

    def __str__(self):
        return 'Оценка для {}'.format(self.visual_novel.title)


class VNGenre(models.Model):
    visual_novel = models.ForeignKey(VisualNovel, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genres_set')
    weight = models.IntegerField(verbose_name='вес', default=0)

    class Meta:
        db_table = 'vns_to_genres'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.genre.title


class VNTag(models.Model):
    visual_novel = models.ForeignKey(VisualNovel, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tags_set')
    weight = models.IntegerField(verbose_name='вес', default=0)

    class Meta:
        db_table = 'vns_to_tags'
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.tag.title


class VNStudio(models.Model):
    visual_novel = models.ForeignKey(VisualNovel, on_delete=models.CASCADE)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='studios_set')
    weight = models.IntegerField(verbose_name='вес', default=0)

    class Meta:
        db_table = 'vns_to_studios'
        verbose_name = 'Студия'
        verbose_name_plural = 'Студии'

    def __str__(self):
        return self.studio.title


class VNStaff(models.Model):
    visual_novel = models.ForeignKey(VisualNovel, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_set')
    role = models.ForeignKey(StaffRole, on_delete=models.PROTECT)
    weight = models.IntegerField(verbose_name='вес', default=0)

    class Meta:
        db_table = 'vns_to_staff'
        verbose_name = 'Создатель'
        verbose_name_plural = 'Создатели'

    def __str__(self):
        return self.staff.title


class VNScreenshot(PublishFileModel):
    title = models.CharField(verbose_name='подпись', max_length=256, null=True, blank=True)
    image = ImageFieldWithEnhancedUploadTo(verbose_name='фотография')
    miniature = ImageFieldWithEnhancedUploadTo(verbose_name='миниатюра', editable=False, blank=True)

    class Meta:
        abstract = True
        file_fields = [
            {
                'field_name': 'image',
                'path': settings.MEDIA_VN_SCREENSHOTS_DIRECTORY
            },
            {
                'field_name': 'miniature',
                'path': settings.MEDIA_VN_SCREENSHOTS_MINI_DIRECTORY
            }
        ]

    def update_miniature(self, mini_width=150):
        if not self.image:
            return
        filename = os.path.basename(self.image.name)
        path = os.path.join(settings.MEDIA_VN_SCREENSHOTS_MINI_DIRECTORY, filename)
        new_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.isfile(new_path):
            return
        image = Image.open(self.image.path)
        th_image = image.copy()
        size = (mini_width, int(float(mini_width) * float(self.image.height) / float(self.image.width)))
        th_image.thumbnail(size, Image.ANTIALIAS)
        th_image.save(new_path)
        self.miniature = path
        return path

    def additional_action_on_save(self, list_of_changed_image_fields, created):
        if 'image' in list_of_changed_image_fields:
            self.delete_files(['miniature'])
        try:
            path = self.image.path
            self.update_miniature()
        except ValueError:
            return
