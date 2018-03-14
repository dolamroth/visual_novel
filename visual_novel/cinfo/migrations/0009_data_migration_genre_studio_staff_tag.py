from __future__ import unicode_literals

from django.db import migrations


def add_genres(apps, schema_editor):
    Genre = apps.get_model('cinfo', 'Genre')
    drama, _ = Genre.objects.get_or_create(title='драма', alias='drama')
    romance, _ = Genre.objects.get_or_create(title='романтика', alias='romance')
    everyday_life, _ = Genre.objects.get_or_create(title='повседневность', alias='everyday_life')
    comedy, _ = Genre.objects.get_or_create(title='комедия', alias='comedy')
    mystic, _ = Genre.objects.get_or_create(title='мистика', alias='mystic')
    action, _ = Genre.objects.get_or_create(title='экшн', alias='action')
    post_apocalyptic, _ = Genre.objects.get_or_create(title='постапокалиптика', alias='post-apocalyptic')
    surrealism, _ = Genre.objects.get_or_create(title='сюрреализм', alias='surrealism')
    fantasy, _ = Genre.objects.get_or_create(title='фэнтези', alias='fantasy')
    metaproject, _ = Genre.objects.get_or_create(
        title='метапроза',
        description="""Метапроза, иногда также <i>метаповествование</i> и <i>метафикшн</i> 
                    (англ. "metafiction")&nbsp;&#8211; литературное произведение, важнейшим 
                    предметом которого является сам процесс его разворачивания, исследование природы 
                    литературного текста.""",
        alias='metaproject'
    )
    horror, _ = Genre.objects.get_or_create(title='хоррор', alias='horror')
    thriller, _ = Genre.objects.get_or_create(title='триллер', alias='thriller')
    sci_fi, _ = Genre.objects.get_or_create(title='научная фантастика', alias='sci-fi')
    detective, _ = Genre.objects.get_or_create(title='детектив', alias='detective')
    dystopia, _ = Genre.objects.get_or_create(title='антиутопия', alias='dystopia')
    war, _ = Genre.objects.get_or_create(title='война', alias='war')


class Migration(migrations.Migration):

    dependencies = [
        ('cinfo', '0008_add_alias_field'),
    ]

    operations = [
        migrations.RunPython(add_genres),
    ]