# Generated by Django 2.0.2 on 2018-08-04 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('translation', '0005_add_translation_item_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranslationBetaLinkSendToVK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vk_group_id', models.CharField(default='', max_length=255, verbose_name='ID группы ВК')),
                ('post_date', models.DateField(auto_now_add=True, verbose_name='Дата')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='translation.TranslationBetaLink', verbose_name='Ссылка на патч')),
            ],
            options={
                'verbose_name': 'Бетассылка, отправленная в группу ВК',
                'verbose_name_plural': 'Бетассылки, отправленные в группы ВК',
                'db_table': 'translation_betalink_send_to_vk',
            },
        ),
    ]
