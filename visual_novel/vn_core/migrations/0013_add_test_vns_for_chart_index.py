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
    mystery, _ = Genre.objects.get_or_create(title='мистика', alias='mystery')

    nakige = Tag.objects.get(alias='nakige')
    all_age = Tag.objects.get(alias='all-age')
    true_end = Tag.objects.get(alias='has-true-ending')
    adv = Tag.objects.get(alias='adv')
    all_18, _ = Tag.objects.get_or_create(alias='all-18')

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
    naga = Staff.objects.get(alias='na-ga')
    kai = Staff.objects.get(alias='kai')

    very_short = Longevity.objects.get(min_length=None, max_length=2)
    short = Longevity.objects.get(min_length=2, max_length=10)
    average = Longevity.objects.get(min_length=10, max_length=30)
    long = Longevity.objects.get(min_length=30, max_length=50)
    very_long = Longevity.objects.get(min_length=50, max_length=None)

    VisualNovel = apps.get_model('vn_core', 'VisualNovel')
    VNGenre = apps.get_model('vn_core', 'VNGenre')
    VNTag = apps.get_model('vn_core', 'VNTag')
    VNStudio = apps.get_model('vn_core', 'VNStudio')
    VNStaff = apps.get_model('vn_core', 'VNStaff')

    # Angel Beats!
    angel_beats, _ = VisualNovel.objects.get_or_create(
        title="Angel Beats! -1st beat-",
        alternative_title="エンジェルビーツ! / Ангельские ритмы!",
        description="""Забавно, но, несмотря на огромную продолжительность человеческой истории, конечного смысла в жизни человека нет. И пусть его нет, но ведь жить-то можно и так, тем более что от жизни-то, особенно будучи молодым, можно и удовольствие получать.<br><br>Можно. Но не всегда. Не удалось оно, жизнью насладиться. Значит, ни смысла, ни удовольствия? А что если... Если выпал шанс на отработку? Смысл можно пока и отложить, а вот поразвлечься стоит – всё равно ты ничего в происходящем не понимаешь. Или не стоит? Или не получится? Воспоминания – штука навязчивая. Хотя...<br><br>А что тебе вообще не хватало? Что для тебя счастье и совершив что, ты готов закончить свою жизнь? Друзья? Семейная жизнь? Деньги? Учёба? Музыка? Полный желудок?<br><br>Если ты узнаешь, что ты не один? Пойдёшь помогать другим? Или проявишь немного эгоизма?<br>...<br>...<br>— «Добро пожаловать во «Фронт отрицающих смерть». Понимаю, это несколько неожиданно, но не хочешь ли ты к нам присоединиться?»<br><br>Решай. Ну, или позволь другим решить за тебя, по течению тоже можно плыть.""",
        date_of_release=datetime.date(2015, 6, 26),
        vndb_id=13774,
        steam_link="",
        alias="angel-beats",
        longevity=average
    )

    angel_beats.save()

    genre, _ = VNGenre.objects.get_or_create(visual_novel=angel_beats, genre=comedy, weight=100)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=angel_beats, genre=drama, weight=65)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=angel_beats, genre=romance, weight=40)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=angel_beats, genre=mystery, weight=70)

    tag, _ = VNTag.objects.get_or_create(visual_novel=angel_beats, tag=nakige, weight=90)
    tag, _ = VNTag.objects.get_or_create(visual_novel=angel_beats, tag=all_age, weight=10)
    tag, _ = VNTag.objects.get_or_create(visual_novel=angel_beats, tag=adv, weight=0)
    tag, _ = VNTag.objects.get_or_create(visual_novel=angel_beats, tag=true_end, weight=20)

    studio, _ = VNStudio.objects.get_or_create(visual_novel=angel_beats, studio=visual_artskey, weight=100)

    staff, _ = VNStaff.objects.get_or_create(visual_novel=angel_beats, staff=maeda_dzun, role=screenwriter, weight=100)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=angel_beats, staff=maeda_dzun, role=composer, weight=70)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=angel_beats, staff=orito_sindzi, role=composer, weight=60)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=angel_beats, staff=naga, role=chardiz, weight=50)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=angel_beats, staff=kai, role=screenwriter, weight=80)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=angel_beats, staff=kagami_esihoki, role=screenwriter, weight=75)

    # Air
    air, _ = VisualNovel.objects.get_or_create(
        title="Air",
        alternative_title="Высь",
        description="""Кунисаки Юкито унаследовал от матери таинственную силу передвигать предметы, не касаясь их, и древнее предание о девушке, живущей в небе. В её поисках он странствует по стране, пока волей судьбы его не заносит в небольшой прибрежный городок. Здесь он встречает нескольких девушек, объединённых мечтой о небе. Возможно ли, что одна из них&nbsp;&#8211; та, которую он ищет? Тем более, что небо в этом городе находится так близко к земле...""",
        date_of_release=datetime.date(2001, 7, 19),
        vndb_id=36,
        steam_link="",
        alias="air",
        longevity=average
    )

    genre, _ = VNGenre.objects.get_or_create(visual_novel=air, genre=comedy, weight=75)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=air, genre=drama, weight=90)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=air, genre=romance, weight=100)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=air, genre=mystery, weight=70)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=air, genre=everyday_life, weight=80)

    tag, _ = VNTag.objects.get_or_create(visual_novel=air, tag=nakige, weight=90)
    tag, _ = VNTag.objects.get_or_create(visual_novel=air, tag=all_18, weight=10)
    tag, _ = VNTag.objects.get_or_create(visual_novel=air, tag=adv, weight=0)
    tag, _ = VNTag.objects.get_or_create(visual_novel=air, tag=true_end, weight=20)

    studio, _ = VNStudio.objects.get_or_create(visual_novel=air, studio=visual_artskey, weight=100)

    staff, _ = VNStaff.objects.get_or_create(visual_novel=air, staff=maeda_dzun, role=screenwriter, weight=100)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=air, staff=maeda_dzun, role=composer, weight=60)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=air, staff=orito_sindzi, role=composer, weight=75)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=air, staff=hinou_itau, role=painter, weight=60)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=air, staff=hinou_itau, role=chardiz, weight=55)


class Migration(migrations.Migration):

    dependencies = [
        ('vn_core', '0012_test-data-migration'),
    ]

    operations = [
        migrations.RunPython(add_test_visual_novel, migrations.RunPython.noop),
    ]
