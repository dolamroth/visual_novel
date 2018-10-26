from celery import shared_task

from django.conf import settings

from notifications.models import MailingTask

from .models import Profile


@shared_task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT,
             soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT)
def update_profile_notification_preferences(self, profile_id, old_weekmap, old_hour):
    profile = Profile.objects.get(id=profile_id)
    new_weekmap = int(profile.weekdays)
    new_hour = profile.send_hour

    pairs_weekday_hour_check_to_create = list()
    pairs_weekday_hour_check_to_delete = list()

    weekmap_xor = new_weekmap ^ old_weekmap
    weekdays_bitwise = [1, 2, 4, 8, 16, 32, 64]
    # If hour hasn't changed, only traverse among A\B and B\A sets, where A, B are new/old weekmaps
    if new_hour == old_hour:
        weekdays_to_check_to_delete = old_weekmap & weekmap_xor
        weekdays_to_check_to_create = new_weekmap & weekmap_xor
        k = 0
        for weekday_bitwise in weekdays_bitwise:
            if weekday_bitwise & weekdays_to_check_to_delete:
                pairs_weekday_hour_check_to_delete.append({
                    'weekday': k,
                    'hour': old_hour
                })
            if weekday_bitwise & weekdays_to_check_to_create:
                pairs_weekday_hour_check_to_create.append({
                    'weekday': k,
                    'hour': old_hour
                })
            k += 1
    # If hour has changed, traverse among pairs (old_weekmap, old_hour) and (new_weekmap, new_hour)
    else:
        k = 0
        for weekday_bitwise in weekdays_bitwise:
            if weekday_bitwise & old_weekmap:
                pairs_weekday_hour_check_to_delete.append({
                    'weekday': k,
                    'hour': old_hour
                })
            if weekday_bitwise & new_weekmap:
                pairs_weekday_hour_check_to_create.append({
                    'weekday': k,
                    'hour': new_hour
                })
            k += 1

    for pair in pairs_weekday_hour_check_to_delete:
        weekday_flags = Profile.weekdays._flags
        clients_count = Profile.objects.filter(
            weekdays=Profile.weekdays.__getattr__(weekday_flags[pair['weekday']]),
            send_hour=old_hour
        ).count()
        if clients_count == 0:
            try:
                mailing_task = MailingTask.objects.get(send_weekday=pair['weekday'], send_hour=old_hour)
                mailing_task.delete()
            except MailingTask.DoesNotExist:
                pass

    for pair in pairs_weekday_hour_check_to_create:
        mailing_task, _ = MailingTask.objects.get_or_create(
            send_weekday=pair['weekday'],
            send_hour=new_hour
        )
