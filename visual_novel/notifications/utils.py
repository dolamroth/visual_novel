from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask
from kombu.utils.json import dumps

from . import WEEKDAYS_RU, WEEKDAYS_CRON


def _create_crontab_schedule(utc_hour, day_of_week):

    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=0,
        hour=utc_hour,
        day_of_week=WEEKDAYS_CRON[day_of_week],
        day_of_month='*',
        month_of_year='*',
    )
    return crontab_schedule


def create_mailing_to_users_task(hour, day_of_week, mailing_task):

    crontab_schedule = _create_crontab_schedule(hour, day_of_week)

    task = PeriodicTask.objects.create(
        crontab=crontab_schedule,
        name='Рассылка статистики в {day_of_week} на {hour} часов'.format(
            day_of_week=WEEKDAYS_RU[day_of_week], hour=hour
        ),
        task='notifications.tasks.send_statistics_task',
        kwargs=dumps({'mailing_task_id': mailing_task.id})
    )

    return task
