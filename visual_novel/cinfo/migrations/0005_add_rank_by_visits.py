# Generated by Django 2.0.2 on 2018-08-15 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinfo', '0004_add_link_to_translators'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='rank_by_visits',
            field=models.IntegerField(blank=True, null=True, verbose_name='место по визитам'),
        ),
        migrations.AddField(
            model_name='staff',
            name='rank_by_visits',
            field=models.IntegerField(blank=True, null=True, verbose_name='место по визитам'),
        ),
        migrations.AddField(
            model_name='studio',
            name='rank_by_visits',
            field=models.IntegerField(blank=True, null=True, verbose_name='место по визитам'),
        ),
        migrations.AddField(
            model_name='tag',
            name='rank_by_visits',
            field=models.IntegerField(blank=True, null=True, verbose_name='место по визитам'),
        ),
    ]
