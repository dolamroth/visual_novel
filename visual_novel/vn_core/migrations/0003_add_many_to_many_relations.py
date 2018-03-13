# Generated by Django 2.0.2 on 2018-03-13 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinfo', '0007_add_longevity_model'),
        ('vn_core', '0002_add_longevity_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='VNGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=0, verbose_name='вес')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='genres_set', to='cinfo.Genre')),
                ('visual_novel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vn_core.VisualNovel')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'db_table': 'vns_to_genres',
            },
        ),
        migrations.CreateModel(
            name='VNStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=0, verbose_name='вес')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cinfo.StaffRole')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='staff_set', to='cinfo.Staff')),
                ('visual_novel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vn_core.VisualNovel')),
            ],
            options={
                'verbose_name': 'Создатель',
                'verbose_name_plural': 'Создатели',
                'db_table': 'vns_to_staff',
            },
        ),
        migrations.CreateModel(
            name='VNStudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=0, verbose_name='вес')),
                ('studio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='studios_set', to='cinfo.Studio')),
                ('visual_novel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vn_core.VisualNovel')),
            ],
            options={
                'verbose_name': 'Студия',
                'verbose_name_plural': 'Студии',
                'db_table': 'vns_to_studios',
            },
        ),
        migrations.CreateModel(
            name='VNTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=0, verbose_name='вес')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tags_set', to='cinfo.Tag')),
                ('visual_novel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vn_core.VisualNovel')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'db_table': 'vns_to_tags',
            },
        ),
        migrations.AddField(
            model_name='visualnovel',
            name='genres',
            field=models.ManyToManyField(through='vn_core.VNGenre', to='cinfo.Genre', verbose_name='жанры'),
        ),
        migrations.AddField(
            model_name='visualnovel',
            name='staff',
            field=models.ManyToManyField(through='vn_core.VNStaff', to='cinfo.Staff', verbose_name='создатели'),
        ),
        migrations.AddField(
            model_name='visualnovel',
            name='studios',
            field=models.ManyToManyField(through='vn_core.VNStudio', to='cinfo.Studio', verbose_name='студии'),
        ),
        migrations.AddField(
            model_name='visualnovel',
            name='tags',
            field=models.ManyToManyField(through='vn_core.VNTag', to='cinfo.Tag', verbose_name='тэги'),
        ),
    ]
