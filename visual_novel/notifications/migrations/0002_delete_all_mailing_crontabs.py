from __future__ import unicode_literals

from django.db import migrations


def delete_crontabs(apps, schema_editor):
    MailingTask = apps.get_model('notifications', 'MailingTask')
    MailingTask.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_add_mailing_task_model'),
    ]

    operations = [
        migrations.RunPython(delete_crontabs, migrations.RunPython.noop),
    ]
