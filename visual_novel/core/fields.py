import datetime
import posixpath

from django.db.models import ImageField, FileField

from .utils import file_directory_path


class ImageFieldWithEnhancedUploadTo(ImageField):
    def __init__(self, verbose_name=None, name=None, storage=None, **kwargs):
        # To secure from the case, when 'upload_to' is passed by force.
        kwargs.pop('upload_to', None)
        kwargs['upload_to'] = file_directory_path
        super(ImageFieldWithEnhancedUploadTo, self).__init__(
            verbose_name=verbose_name, name=name, storage=storage, **kwargs
        )

    def deconstruct(self):
        name, path, args, kwargs = super(ImageFieldWithEnhancedUploadTo, self).deconstruct()
        # Deleting 'upload_to' attribute is necessary for Django to stop spawning migrations for ImageFields.
        del kwargs['upload_to']
        return name, path, args, kwargs

    def generate_filename(self, instance, filename):
        if callable(self.upload_to):
            # The only difference is to pass Field instance (self) to upload_to function
            filename = self.upload_to(self, instance, filename)
        else:
            dirname = datetime.datetime.now().strftime(self.upload_to)
            filename = posixpath.join(dirname, filename)
        return self.storage.generate_filename(filename)


class FileFieldWithEnhancedUploadTo(FileField):
    def __init__(self, verbose_name=None, name=None, storage=None, **kwargs):
        # To secure from the case, when 'upload_to' is passed by force.
        kwargs.pop('upload_to', None)
        kwargs['upload_to'] = file_directory_path
        super(FileFieldWithEnhancedUploadTo, self).__init__(
            verbose_name=verbose_name, name=name, storage=storage, **kwargs
        )

    def deconstruct(self):
        name, path, args, kwargs = super(FileFieldWithEnhancedUploadTo, self).deconstruct()
        # Deleting 'upload_to' attribute is necessary for Django to stop spawning migrations for FileFields.
        del kwargs['upload_to']
        return name, path, args, kwargs

    def generate_filename(self, instance, filename):
        if callable(self.upload_to):
            # The only difference is to pass Field instance (self) to upload_to function
            filename = self.upload_to(self, instance, filename)
        else:
            dirname = datetime.datetime.now().strftime(self.upload_to)
            filename = posixpath.join(dirname, filename)
        return self.storage.generate_filename(filename)