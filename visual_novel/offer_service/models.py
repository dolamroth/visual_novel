from django.db import models
from core.models import PublishModel
from django.core.exceptions import ValidationError
from notifications.service import send_email


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

    def __init__(self, *args, **kwargs):
        super(Offer, self).__init__(*args, **kwargs)
        self.__important_fields = ['is_considered', 'is_accepted', 'is_rejected']
        for field in self.__important_fields:
            setattr(self, '__original_%s' % field, getattr(self, field))

    def has_changed(self):
        for field in self.__important_fields:
            orig = '__original_%s' % field
            if getattr(self, orig) != getattr(self, field):
                return True, field
        return False, 'test'

    def save(self, *args, **kwargs):
        if self.is_accepted or self.is_rejected:
            self.is_published = False
        super(Offer, self).save(*args, **kwargs)
        flag, type_email = self.has_changed()
        # TODO more complex and informative text
        # TODO add celery apply_async for speed 
        if flag and type_email == 'is_considered':
            send_email('Заявка', 'Ваша заявка принята к рассмотрению.', self.email)
        if flag and type_email == 'is_accepted':
            send_email('Заявка', 'Ваша заявка принята администрацией.', self.email)
        if flag and type_email == 'is_rejected':
            send_email('Заявка', 'Ваша заявка отклонена, нам жаль (нет).', self.email)
