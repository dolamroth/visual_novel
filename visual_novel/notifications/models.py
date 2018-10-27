from django_celery_beat.models import PeriodicTask
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from . import WEEKDAYS_RU
from .utils import create_mailing_to_users_task


class MailingTask(models.Model):
    mailing_task = models.OneToOneField(PeriodicTask, on_delete=models.PROTECT,
                                                  verbose_name='Задача автоматической рассылки', blank=False,
                                                  editable=False, null=True)
    send_hour = models.IntegerField(verbose_name='Час рассылки',
                                    validators=[MaxValueValidator(23), MinValueValidator(0)])
    send_weekday = models.IntegerField(verbose_name='День недели рассылки',
                                    validators=[MaxValueValidator(6), MinValueValidator(0)])

    class Meta:
        verbose_name = "Рассылка статистики"
        verbose_name_plural = "Рассылки статистики"

    def __str__(self):
        return 'Рассылка на {} часов в {}'.format(self.send_hour, WEEKDAYS_RU[self.send_weekday])

    def save(self, *args, **kwargs):
        super(MailingTask, self).save(*args, **kwargs)
        if not self.mailing_task:
            self.mailing_task = create_mailing_to_users_task(
                hour=self.send_hour,
                day_of_week=self.send_weekday,
                mailing_task=self
            )

    def delete(self, *args, **kwargs):
        mailing_task = self.mailing_task
        super(MailingTask, self).delete(*args, **kwargs)
        mailing_task.delete()
