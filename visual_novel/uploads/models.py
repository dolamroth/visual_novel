import os

from django.db import models
from django.conf import settings

from core.fields import FileFieldWithEnhancedUploadTo
from core.models import PublishFileModel


class Upload(PublishFileModel):
    title = models.CharField(verbose_name='название', max_length=500)
    file = FileFieldWithEnhancedUploadTo(verbose_name='файл')
    extension = models.CharField(verbose_name='расширение', default='', blank=True, editable=False, max_length=20)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'закачка'
        verbose_name_plural = 'закачки'
        file_fields = [
            {'field_name': 'file',
             'path': settings.MEDIA_CUSTOM_FILES_DIRECTORY}
        ]
        db_table = 'custom_downloads'

    def get_site_url(self):
        return settings.MEDIA_URL + str(self.file)

    def __str__(self):
        return self.title

    def action_after_file_save(self, list_of_changed_image_fields, created):
        if self.file:
            extension = os.path.splitext(self.file.path)[1]
            self.extension = extension
            super(PublishFileModel, self).save()

    def is_image(self):
        return self.extension in ['.jpeg', '.jpg', '.png', '.gif', '.tiff']
