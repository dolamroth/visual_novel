from __future__ import unicode_literals

from django.db import migrations


def update_profiles(apps, schema_editor):
    Profile = apps.get_model('core', 'Profile')
    Profile.objects.update(email_confirmed=True)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_email_is_confirmed_field'),
    ]

    operations = [
        migrations.RunPython(update_profiles, migrations.RunPython.noop),
    ]
