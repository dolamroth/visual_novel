from celery import shared_task

from django.conf import settings

from core.models import Profile

from .models import MailingTask


@shared_task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT,
             soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT)
def send_statistics_task(self, mailing_task_id):
    mailing_task = MailingTask.objects.get(id=mailing_task_id)
    weekmap = Profile.weekdays._flags
    send_hour = mailing_task.send_hour
    users_to_send = Profile.objects.filter(
        send_hour=send_hour,
        weekdays=Profile.weekdays.__getattr__(weekmap[mailing_task.send_weekday])
    )
