# Generated by Django 2.0.2 on 2018-07-14 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinfo', '0004_add_link_to_translators'),
        ('translation', '0002_translationitemsendtovk'),
    ]

    operations = [
        migrations.AddField(
            model_name='translationitem',
            name='translator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cinfo.Translator', verbose_name='Переводчик'),
        ),
    ]
