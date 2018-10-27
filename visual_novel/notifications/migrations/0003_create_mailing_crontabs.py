from __future__ import unicode_literals

from django.db import migrations


def create_mailing_tasks_crontabs(apps, schema_editor):
    MailingTask = apps.get_model('notifications', 'MailingTask')
    # For all weekdays
    for d in range(0, 7):
        for h in range(0, 24):
            m, _ = MailingTask.objects.get_or_create(send_hour=h, send_weekday=d)
            m.save()


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_delete_all_mailing_crontabs'),
        ('core', '0006_delete_notification_settings_for_all'),
    ]

    operations = [
        migrations.RunPython(create_mailing_tasks_crontabs, migrations.RunPython.noop),
    ]
