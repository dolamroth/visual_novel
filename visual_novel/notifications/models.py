from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from . import WEEKDAYS_RU


class MailingTask(models.Model):
    send_hour = models.IntegerField(verbose_name='Час рассылки',
                                    validators=[MaxValueValidator(23), MinValueValidator(0)])
    send_weekday = models.IntegerField(verbose_name='День недели рассылки',
                                    validators=[MaxValueValidator(6), MinValueValidator(0)])

    class Meta:
        verbose_name = "Рассылка статистики"
        verbose_name_plural = "Рассылки статистики"

    def __str__(self):
        return 'Рассылка на {} часов в {}'.format(self.send_hour, WEEKDAYS_RU[self.send_weekday])
