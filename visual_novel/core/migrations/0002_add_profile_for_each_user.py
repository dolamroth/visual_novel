from __future__ import unicode_literals

from django.db import migrations


def add_profiles(apps, schema_editor):
    Profile = apps.get_model('core', 'Profile')
    User = apps.get_model('auth', 'User')

    for user in User.objects.all():
        profile, _ = Profile.objects.get_or_create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_add_profile_model'),
    ]

    operations = [
        migrations.RunPython(add_profiles, migrations.RunPython.noop),
    ]
