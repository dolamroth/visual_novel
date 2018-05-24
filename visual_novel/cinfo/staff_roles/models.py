from django.db import models

from core.models import PublishModel


class StaffRole(PublishModel):
    title = models.CharField(verbose_name='название', max_length=256)

    class Meta:
        db_table = 'staff_roles'
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.title
