# Generated by Django 2.0.2 on 2018-04-26 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translation', '0001_new_translation_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='translationbetalink',
            options={'verbose_name': 'Ссылка на патч', 'verbose_name_plural': 'Ссылки на патчи'},
        ),
    ]
