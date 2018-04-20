from bitfield import BitField
import datetime

from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from timezone_field import TimeZoneField


class PublishQuerySet(QuerySet):
    def __init__(self, model=None, query=None, using=None):
        super(PublishQuerySet, self).__init__(model, query)

    def published(self, *args, **kwargs):
        return self.filter(is_published=True, **kwargs)

    def visible(self, **kwargs):
        return self.published(**kwargs)


class PublishManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return PublishQuerySet(self.model)

    def published(self, *args, **kwargs):
        return self.get_query_set().published(*args, **kwargs)


class PublishModel(models.Model):
    is_published = models.BooleanField(verbose_name='публикация', default=True)

    objects = PublishManager()

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = TimeZoneField(default=settings.DEFAULT_TIME_ZONE)
    email_confirmed = models.BooleanField(default=False)
    send_distributions = models.BooleanField(verbose_name='Отправлять рассылку', default=False)
    send_time = models.TimeField(verbose_name='Время рассылки', default=datetime.time(10, 30))
    weekdays = BitField(verbose_name='Битовый код дней рассылки',
                        flags=(('monday', 'Понедельник'), ('tuesday', 'Вторник'), ('wednesday', 'Среда'),
                               ('thursday', 'Четверг'), ('friday', 'Пятница'), ('saturday', 'Суббота'),
                               ('sunday', 'Воскреснье')), default=127)

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
        Profile.objects.create(user=instance)
    instance.profile.save()
