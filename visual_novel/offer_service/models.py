from django.db import models
from core.models import PublishModel
from django.core.exceptions import ValidationError


class Offer(PublishModel):
    name = models.CharField(verbose_name='название', blank=True, null=True, max_length=256, default='пользователь')
    offer = models.TextField(verbose_name='предложение', max_length=5000, default='')
    email = models.CharField(verbose_name='почта', max_length=256)
    is_considered = models.BooleanField(verbose_name='Рассмотрено', default=False)
    is_accepted = models.BooleanField(verbose_name='Принято', default=False)
    is_rejected = models.BooleanField(verbose_name='Отказано', default=False)
    rejected_reasons = models.TextField(verbose_name='Причины отказа', max_length=5000, null=True, blank=True)
    timestamp = models.DateTimeField(verbose_name='Время заявки', auto_now_add=True, editable=False)

    class Meta:
        db_table = 'offers'
        verbose_name = 'Предложение по улучшению сайта'
        verbose_name_plural = 'Предложения по улучшению сайта'

    def __str__(self):
        return 'Заявка от %s %s' % (self.email, self.timestamp.strftime("%d/%m/%y %H:%M"))

    def save(self, *args, **kwargs):
        if self.is_accepted or self.is_rejected:
            self.is_published = False
        super(Offer, self).save(*args, **kwargs)

