from __future__ import unicode_literals

from django.db import migrations


def add_longevity_info(apps, schema_editor):
    Longevity = apps.get_model('cinfo', 'Longevity')

    very_short, _ = Longevity.objects.get_or_create(
        title="очень короткая",
        min_length = None,
        max_length = 2
    )
    short, _ = Longevity.objects.get_or_create(
        title="короткая",
        min_length=2,
        max_length=10
    )
    average, _ = Longevity.objects.get_or_create(
        title="средняя",
        min_length=10,
        max_length=30
    )
    long, _ = Longevity.objects.get_or_create(
        title="длинная",
        min_length=30,
        max_length=50
    )
    very_long, _ = Longevity.objects.get_or_create(
        title="очень длинная",
        min_length=50,
        max_length=None
    )


class Migration(migrations.Migration):

    dependencies = [
        ('cinfo', '0009_data_migration_genre_studio_staff_tag'),
    ]

    operations = [
        migrations.RunPython(add_longevity_info, migrations.RunPython.noop),
    ]
