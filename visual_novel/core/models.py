from bitfield import BitField

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from timezone_field import TimeZoneField

ALL_WEEKDAYS_BITMAP = 127


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = TimeZoneField(default=settings.DEFAULT_TIME_ZONE)
    email_confirmed = models.BooleanField(default=False)
    send_distributions = models.BooleanField(verbose_name='Отправлять рассылку', default=False)
    send_time = models.TimeField(verbose_name='Время рассылки', default=settings.DEFAULT_MAILING_SEND_TIME)
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
