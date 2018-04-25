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

    angel_beats = VisualNovel.objects.get(alias="angel-beats")
    angel_beats_chart, _ = ChartItem.objects.get_or_create(
        visual_novel=angel_beats,
        date_of_translation=datetime.date(2017, 1, 22)
    )

    air = VisualNovel.objects.get(alias="air")
    air_chart, _ = ChartItem.objects.get_or_create(
        visual_novel=air,
        date_of_translation=datetime.date(2015, 9, 22)
    )

    rewrite = VisualNovel.objects.get(alias="rewrite")
    rewrite_chart, _ = ChartItem.objects.get_or_create(
        visual_novel=rewrite,
        date_of_translation=datetime.date(2016, 12, 11)
    )

    swan_song = VisualNovel.objects.get(alias="swan-song")
    swan_song_chart, _ = ChartItem.objects.get_or_create(
        visual_novel=swan_song,
        date_of_translation=datetime.date(2014, 5, 20)
    )

    forest = VisualNovel.objects.get(alias="forest")
    forest_chart, _ = ChartItem.objects.get_or_create(
        visual_novel=forest,
        date_of_translation=datetime.date(2017, 2, 3)
    )


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0001_new_chart_model'),
        ('vn_core', '0002_test_data'),
    ]

    operations = [
        migrations.RunPython(add_test_chartitem, migrations.RunPython.noop),
    ]
