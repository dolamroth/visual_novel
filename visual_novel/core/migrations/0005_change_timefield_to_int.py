# Generated by Django 2.0.2 on 2018-08-23 09:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_add_vk_id_to_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='send_time',
        ),
        migrations.AddField(
            model_name='profile',
            name='send_hour',
            field=models.IntegerField(default=16, validators=[django.core.validators.MaxValueValidator(23), django.core.validators.MinValueValidator(0)], verbose_name='Час рассылки'),
        ),
    ]
