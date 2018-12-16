import os
from bitfield import BitField
from constance import config

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
import django.db.models.options as options
from django.dispatch import receiver

from timezone_field import TimeZoneField
from notifications.vk import VK

ALL_WEEKDAYS_BITMAP = 127

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('file_fields',)


class PublishModel(models.Model):
    is_published = models.BooleanField(verbose_name='публикация', default=True)

    class Meta:
        abstract = True

    def publish(self):
        self.is_published = True
        super(PublishModel, self).save()

    def unpublish(self):
        self.is_published = False
        super(PublishModel, self).save()


class PublishFileQuerySet(models.query.QuerySet):
    def delete(self):
        for d in self:
            list_of_image_fields = [f['field_name'] for f in d._meta.__dict__.get('file_fields', [])]
            d.delete_files(list_of_image_fields)
        super(PublishFileQuerySet, self).delete()


class PublishFileManager(models.Manager):
    def get_queryset(self):
        return PublishFileQuerySet(self.model, using=self._db)


class PublishFileModel(PublishModel):

    objects = PublishFileManager()

    class Meta:
        abstract = True

    def delete_files(self, list_of_fieldnames=list()):
        model = self.__class__
        try:
            obj = model.objects.get(pk=self.pk)
        except model.DoesNotExist:
            return
        # Delete all selected image fields within a model
        for field in list_of_fieldnames:
            try:
                # path = obj._meta.get_field(field).path
                path = getattr(obj, field).path
                if os.path.isfile(path):
                    os.remove(path)
            except ValueError:
                pass

    def get_old_file_path_if_changed(self):
        model = self.__class__
        list_of_field_names = list()
        try:
            instance = model.objects.get(pk=self.pk)
        except model.DoesNotExist:
            return list()

        for field in instance._meta.__dict__.get('file_fields', []):
            fieldname = field['field_name']
            try:
                new_path = getattr(self, fieldname).path
            except ValueError:
                new_path = ''
            try:
                old_path = getattr(instance, fieldname).path
            except ValueError:
                old_path = ''
            if new_path != old_path:
                list_of_field_names.append(fieldname)
        return list_of_field_names

    def additional_action_on_save(self, list_of_changed_image_fields, created):
        """
        To be overwritten in child models.
        """
        pass

    def save(self, *args, **kwargs):
        created = not self.id
        list_of_changed_image_fields = self.get_old_file_path_if_changed()
        self.delete_files(list_of_changed_image_fields)
        super(PublishModel, self).save(*args, **kwargs)
        self.additional_action_on_save(list_of_changed_image_fields, created)
        super(PublishModel, self).save()

    def delete(self, *args, **kwargs):
        list_of_image_fields = [d['field_name'] for d in self._meta.__dict__.get('file_fields', [])]
        self.delete_files(list_of_image_fields)
        super(PublishModel, self).save(*args, **kwargs)
        super(PublishModel, self).delete(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    timezone = TimeZoneField(default=settings.DEFAULT_TIME_ZONE, verbose_name='Временная зона')
    email_confirmed = models.BooleanField(default=False, verbose_name='Email подтвержден')
    send_distributions = models.BooleanField(verbose_name='Отправлять рассылку', default=False)
    send_hour = models.IntegerField(verbose_name='Час рассылки', default=16,
                                    validators=[MaxValueValidator(23), MinValueValidator(0)])
    weekdays = BitField(verbose_name='Битовый код дней рассылки',
                        flags=(('monday', 'Понедельник'), ('tuesday', 'Вторник'), ('wednesday', 'Среда'),
                               ('thursday', 'Четверг'), ('friday', 'Пятница'), ('saturday', 'Суббота'),
                               ('sunday', 'Воскресенье')), default=ALL_WEEKDAYS_BITMAP)

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return self.user.username

    def is_staff(self):
        return self.user.is_staff
    is_staff.short_description = 'Модератор'

    def is_superuser(self):
        return self.user.is_superuser
    is_superuser.short_description = 'Суперпользователь'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            email_confirmed=instance.is_staff
        )
    instance.profile.save()
