from __future__ import unicode_literals

import datetime

from django.db import migrations


def add_test_visual_novels(apps, schema_editor):
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
    mystery = Genre.objects.get(alias='mystery')
    sci_fi = Genre.objects.get(alias='scifi')
    fantasy = Genre.objects.get(alias='fantasy')
    action = Genre.objects.get(alias='action')
    post_apocalyptic = Genre.objects.get(alias='post-apocalyptic')
    surrealism = Genre.objects.get(alias='surrealism')
    metafiction = Genre.objects.get(alias='metafiction')

    nakige = Tag.objects.get(alias='nakige')
    all_age = Tag.objects.get(alias='all-age')
    true_end = Tag.objects.get(alias='has-true-ending')
    adv = Tag.objects.get(alias='adv')
    all_18 = Tag.objects.get(alias='all-18')
    chuunige = Tag.objects.get(alias='chuunige')
    eroge = Tag.objects.get(alias='eroge')
    nvl = Tag.objects.get(alias='nvl')
    utsuge = Tag.objects.get(alias='utsuge')
    guro = Tag.objects.get(alias='guro')
    madness = Tag.objects.get(alias='madness')
    magic = Tag.objects.get(alias='magic')
    despair = Tag.objects.get(alias='despair')
    linear_plot = Tag.objects.get(alias='linear-plot')

    screenwriter = StaffRole.objects.get(title='сценарист')
    composer = StaffRole.objects.get(title='композитор')
    painter = StaffRole.objects.get(title='художник')
    chardiz = StaffRole.objects.get(title='чардиз')

    visual_artskey = Studio.objects.get(alias='visual-arts-key')
    le_chocolat = Studio.objects.get(alias='le-chocolat')
    liar_soft = Studio.objects.get(alias='liar-soft')

    maeda_dzun = Staff.objects.get(alias='maeda-jun')
    orito_sindzi = Staff.objects.get(alias='orito-shinji')
    hinou_itau = Staff.objects.get(alias='hinoue-itaru')
    tonokava_yto = Staff.objects.get(alias='tonokawa-yuuto')
    kagami_esihoki = Staff.objects.get(alias='kashida-leo')
    naga = Staff.objects.get(alias='na-ga')
    kai = Staff.objects.get(alias='kai')
    ryuukishi07 = Staff.objects.get(alias='ryuukishi07')
    tanaka_romeo = Staff.objects.get(alias='tanaka-romeo')
    setoguchi_renya = Staff.objects.get(alias='setoguchi-renya')
    hoshizora_meteor = Staff.objects.get(alias='hoshizora-meteor')

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
    staff, _ = VNStaff.objects.get_or_create(visual_novel=angel_beats, staff=kagami_esihoki, role=screenwriter,
                                             weight=75)

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

    air.save()

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

    # Rewrite
    rewrite, _ = VisualNovel.objects.get_or_create(
        title="Rewrite",
        alternative_title="リライト / Перезапись",
        description="""Даже в самой благополучной обстановке люди не всегда могут найти себя и своё счастье. Тэннодзи Котаро, учащийся в престижной школе Кадзамацури, самого экологического города мира, стоит на перепутье. С родителями-трудоголиками он видится редко, из друзей у него остались лишь подруга детства, Камбе Котори, и школьный хулиган, Харухико Ёсино, а воспоминания прошлых беззаботных лет пусты и туманны. Не желая упускать юность, Котаро загорается идеей возродить школьный оккультный клуб и затащить туда своих знакомых, где они могли бы выполнять различные квесты, веселиться от души и просто укреплять свою дружбу. Однако, пытаясь обустроить свой идиллический очаг, Котаро начинает ощущать присутствие некой тайны, связывающей его знакомых, Кадзамацури, его собственную мистическую способность "перезаписи" и отрывок воспоминаний, потерянный десять лет назад...""",
        date_of_release=datetime.date(2011, 9, 30),
        vndb_id=751,
        steam_link="",
        alias="rewrite",
        longevity=very_long
    )

    rewrite.save()

    genre, _ = VNGenre.objects.get_or_create(visual_novel=rewrite, genre=sci_fi, weight=100)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=rewrite, genre=fantasy, weight=90)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=rewrite, genre=drama, weight=80)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=rewrite, genre=comedy, weight=70)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=rewrite, genre=mystery, weight=65)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=rewrite, genre=romance, weight=60)

    tag, _ = VNTag.objects.get_or_create(visual_novel=rewrite, tag=chuunige, weight=95)
    tag, _ = VNTag.objects.get_or_create(visual_novel=rewrite, tag=nakige, weight=60)
    tag, _ = VNTag.objects.get_or_create(visual_novel=rewrite, tag=all_age, weight=10)
    tag, _ = VNTag.objects.get_or_create(visual_novel=rewrite, tag=adv, weight=0)
    tag, _ = VNTag.objects.get_or_create(visual_novel=rewrite, tag=true_end, weight=20)

    studio, _ = VNStudio.objects.get_or_create(visual_novel=rewrite, studio=visual_artskey, weight=100)

    staff, _ = VNStaff.objects.get_or_create(visual_novel=rewrite, staff=tanaka_romeo, role=screenwriter, weight=100)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=rewrite, staff=tonokava_yto, role=screenwriter, weight=80)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=rewrite, staff=ryuukishi07, role=screenwriter, weight=60)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=rewrite, staff=hinou_itau, role=painter, weight=55)
    staff, _ = VNStaff.objects.get_or_create(visual_novel=rewrite, staff=hinou_itau, role=chardiz, weight=50)

    # Swan Song
    swan_song, _ = VisualNovel.objects.get_or_create(
        title="Swan Song",
        alternative_title="スワンソング / Лебединая песнь",
        description="""Небольшой городок в предгорьях. Разгар зимы&nbsp;&#8211; 24 декабря. Все заняты мирной подготовкой к наступающим праздникам.<br><br>Студент местного колледжа Амако Цукаса, ночью выходит на улицу, чтобы купить в автомате бутылку газировки, как вдруг начинается сильнейшее землетрясение, и за считанные минуты весь город превращается буквально в руины. В такой сильной катастрофе можно было выжить только чудом. Однако всё же нескольким людям, так же, как и ему, удалось спастись. Первые, кого он находит,&nbsp;&#8211; девушка, страдающая аутизмом, Сака Ароэ, и её старшая сестра, которую он застаёт уже при смерти. Она просит Цукасу позаботиться об Арое, потому что самой ей не выжить. С трудом они добираются до местной церкви&nbsp;&#8211; единственного более или менее уцелевшего здания в городе. Туда же приходят другие уцелевшие. Начинается долгая борьба за выживание&nbsp;&#8211; без электричества, без света, без отопления, без свежей воды...""",
        date_of_release=datetime.date(2005, 7, 29),
        vndb_id=914,
        steam_link="",
        alias="swan-song",
        longevity=average
    )

    swan_song.save()

    genre, _ = VNGenre.objects.get_or_create(visual_novel=swan_song, genre=action, weight=50)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=swan_song, genre=post_apocalyptic, weight=80)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=swan_song, genre=drama, weight=100)

    tag, _ = VNTag.objects.get_or_create(visual_novel=swan_song, tag=utsuge, weight=100)
    tag, _ = VNTag.objects.get_or_create(visual_novel=swan_song, tag=guro, weight=50)
    tag, _ = VNTag.objects.get_or_create(visual_novel=swan_song, tag=madness, weight=80)
    tag, _ = VNTag.objects.get_or_create(visual_novel=swan_song, tag=despair, weight=85)
    tag, _ = VNTag.objects.get_or_create(visual_novel=swan_song, tag=eroge, weight=20)
    tag, _ = VNTag.objects.get_or_create(visual_novel=swan_song, tag=nvl, weight=0)

    studio, _ = VNStudio.objects.get_or_create(visual_novel=swan_song, studio=le_chocolat, weight=100)

    staff, _ = VNStaff.objects.get_or_create(visual_novel=swan_song, staff=setoguchi_renya, role=screenwriter,
                                             weight=100)

    # Forest
    forest, _ = VisualNovel.objects.get_or_create(
        title="Forest",
        alternative_title="フォレスト",
        description="""<i>"Я Алиса. Пожалуйста, расскажи мне сказку."</i><br><br>Тут и там, в переулках между зданиями, глухих закоулках и, быть может, даже под землёй, в наш мир просачивается Лес. Лес&nbsp;&#8211; это запретное место, не подчиняющееся законам нашего мира.<br><br>Наши герои должны противостоять козням Леса, без особой надежды на помощь или понимание со стороны внешнего мира.<br><br>Они сражаются с "загадками", которые на них насылает Лес, используя свои сверхъестественные способности, известные как "дары".<br><br>И, если им будет суждено проиграть, их ждёт то, чего они боятся больше всего на свете,&nbsp;&#8211; изгнание из Синдзюку.""",
        date_of_release=datetime.date(2004, 2, 13),
        vndb_id=599,
        steam_link="",
        alias="forest",
        longevity=average
    )

    forest.save()

    genre, _ = VNGenre.objects.get_or_create(visual_novel=forest, genre=surrealism, weight=80)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=forest, genre=metafiction, weight=90)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=forest, genre=comedy, weight=50)
    genre, _ = VNGenre.objects.get_or_create(visual_novel=forest, genre=fantasy, weight=95)

    tag, _ = VNTag.objects.get_or_create(visual_novel=forest, tag=madness, weight=40)
    tag, _ = VNTag.objects.get_or_create(visual_novel=forest, tag=magic, weight=60)
    tag, _ = VNTag.objects.get_or_create(visual_novel=forest, tag=linear_plot, weight=30)
    tag, _ = VNTag.objects.get_or_create(visual_novel=forest, tag=eroge, weight=20)
    tag, _ = VNTag.objects.get_or_create(visual_novel=forest, tag=adv, weight=0)

    studio, _ = VNStudio.objects.get_or_create(visual_novel=forest, studio=liar_soft, weight=100)

    staff, _ = VNStaff.objects.get_or_create(visual_novel=forest, staff=hoshizora_meteor, role=screenwriter, weight=100)


class Migration(migrations.Migration):

    dependencies = [
        ('vn_core', '0001_base_models_for_visual_novels'),
        ('cinfo', '0002_test_data'),
    ]

    operations = [
        migrations.RunPython(add_test_visual_novels, migrations.RunPython.noop),
    ]
