from __future__ import unicode_literals

import datetime

from django.db import migrations


def add_test_chartitem(apps, schema_editor):
    ChartItem = apps.get_model('chart', 'ChartItem')
    VisualNovel = apps.get_model('vn_core', 'VisualNovel')

    little_busters = VisualNovel.objects.get(alias="little-busters")
    little_busters_chart, _ = ChartItem.objects.get_or_create(
        visual_novel=little_busters,
        date_of_translation=datetime.date(2015, 4, 7)
    )


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0005_add_screenshot_to_chartitem_as_one_to_many'),
    ]

    operations = [
        migrations.RunPython(add_test_chartitem, migrations.RunPython.noop),
    ]
