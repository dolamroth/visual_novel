# Generated by Django 2.0.2 on 2018-07-30 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_new_profile_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_confirmed',
            field=models.BooleanField(default=False, verbose_name='Email подтвержден'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default='Europe/Moscow', verbose_name='Временная зона'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
