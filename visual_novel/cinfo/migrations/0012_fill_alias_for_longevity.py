from __future__ import unicode_literals

from django.db import migrations


def add_longevity_info(apps, schema_editor):
    Longevity = apps.get_model('cinfo', 'Longevity')

    very_short = Longevity.objects.get(min_length=None, max_length=2)
    very_short.alias = 'very-short'
    very_short.save()

    short = Longevity.objects.get(min_length=2, max_length=10)
    short.alias = 'short'
    short.save()

    average = Longevity.objects.get(min_length=10, max_length=30)
    average.alias = 'average'
    average.save()

    long = Longevity.objects.get(min_length=30, max_length=50)
    long.alias = 'long'
    long.save()

    very_long = Longevity.objects.get(min_length=50, max_length=None)
    very_long.alias = 'very-long'
    very_long.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cinfo', '0011_add_alias_field'),
    ]

    operations = [
        migrations.RunPython(add_longevity_info, migrations.RunPython.noop),
    ]
