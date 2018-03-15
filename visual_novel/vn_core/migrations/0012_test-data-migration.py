from __future__ import unicode_literals

import datetime

from django.db import migrations


def add_test_visual_novel(apps, schema_editor):
    Genre = apps.get_model('cinfo', 'Genre')
    Tag = apps.get_model('cinfo', 'Tag')
    StaffRole = apps.get_model('cinfo', 'StaffRole')
    Studio = apps.get_model('cinfo', 'Studio')
    Staff = apps.get_model('cinfo', 'Staff')
    Longevity = apps.get_model('cinfo', 'Longevity')

    drama = Genre.objects.get(alias='drama')
    romance = Genre.objects.get(alias='romance')
    everyday_life = Genre.objects.get(alias='slice-of-life')
    comedy = Genre.objects.get(alias='comedy')

    nakige = Tag.objects.get(alias='nakige')
    all_age = Tag.objects.get(alias='all-age')
    true_end = Tag.objects.get(alias='has-true-ending')
    adv = Tag.objects.get(alias='adv')

    screenwriter = StaffRole.objects.get(title='сценарист')
    composer = StaffRole.objects.get(title='композитор')
    painter = StaffRole.objects.get(title='художник')
    chardiz = StaffRole.objects.get(title='чардиз')

    visual_artskey = Studio.objects.get(alias='visual-arts-key')

    maeda_dzun = Staff.objects.get(alias='maeda-jun')
    orito_sindzi = Staff.objects.get(alias='orito-shinji')
    hinou_itau = Staff.objects.get(alias='hinoue-itaru')
    tonokava_yto = Staff.objects.get(alias='tonokawa-yuuto')
    kagami_esihoki = Staff.objects.get(alias='kashida-leo')

    very_long = Longevity.objects.get(min_length=50)

    VisualNovel = apps.get_model('vn_core', 'VisualNovel')

    little_busters, _ = VisualNovel.objects.get_or_create(
        title="Little busters!",
        alternative_title="Маленькие проказники! / リトルバスターズ！",
        description="""История повествует о Наоэ Рики, ученике старшей школы, в детстве лишившегося родителей и потерявшего веру в жизнь, но вновь обретшего её после знакомства с четырьмя ребятами, называвшими себя "Маленькие проказники". Общаясь и играя с ними, Рики смог пережить терзавшую его боль и вернуться к нормальной жизни. События новеллы происходят в предвыпускном одиннадцатом классе. Ребята по-прежнему дружны и наслаждаются школьной жизнью, но не за горами расставание... Чтобы провести последние школьные годы по полной, они решают сделать невероятное&nbsp;&#8211; собрать команду и сыграть в бейсбол!""",
        date_of_release=datetime.date(2007, 9, 28),
        vndb_id=5,
        steam_link="http://store.steampowered.com/app/635940/",
        alias="little-busters",
        longevity=very_long
    )

    little_busters.save()

    VNGenre = apps.get_model('vn_core', 'VNGenre')
    VNTag = apps.get_model('vn_core', 'VNTag')
    VNStudio = apps.get_model('vn_core', 'VNStudio')
    VNStaff = apps.get_model('vn_core', 'VNStaff')

    genre, _ = VNGenre.objects.get_or_create(visual_novel=little_busters, genre=drama, weight=95)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=little_busters, genre=romance, weight=75)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=little_busters, genre=everyday_life, weight=60)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=little_busters, genre=comedy, weight=80)

    tag, _ = VNTag.objects.get_or_create(visual_novel=little_busters, tag=nakige, weight=95)
    tag, _ = VNTag.objects.get_or_create(visual_novel=little_busters, tag=all_age, weight=10)
    tag, _ = VNTag.objects.get_or_create(visual_novel=little_busters, tag=adv, weight=0)
    tag, _ = VNTag.objects.get_or_create(visual_novel=little_busters, tag=true_end, weight=20)

    studio, _ = VNStudio.objects.get_or_create(visual_novel=little_busters, studio=visual_artskey, weight=100)

    staff, _ = VNStaff.objects.get_or_create(visual_novel=little_busters, staff=maeda_dzun, role=screenwriter, weight=100)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=little_busters, staff=maeda_dzun, role=composer, weight=60)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=little_busters, staff=orito_sindzi, role=composer, weight=80)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=little_busters, staff=hinou_itau, role=painter, weight=70)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=little_busters, staff=hinou_itau, role=chardiz, weight=65)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=little_busters, staff=tonokava_yto, role=screenwriter, weight=90)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=little_busters, staff=kagami_esihoki, role=screenwriter, weight=0)


class Migration(migrations.Migration):

    dependencies = [
        ('vn_core', '0011_vn_poster_nullable'),
        ('cinfo', '0010_add_longevity_info'),
    ]

    operations = [
        migrations.RunPython(add_test_visual_novel, migrations.RunPython.noop),
    ]
