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


def add_tags(apps, schema_editor):
    Tag = apps.get_model('cinfo', 'Tag')
    nakige, _ = Tag.objects.get_or_create(
        title='накиге',
        description="""Накиге (от 泣きゲ, буквально "плачущая игра")&nbsp;&#8211; подвид визуальных новелл, 
                        основанный на идее заставить игрока сопереживать героям, испытать сильные душевные переживания. 
                        Такие игры следуют традиционной формуле: первая комедийная часть игры раскрывает персонажей, 
                        в то время как в основе второй лежат глубоко эмоциональные, пробивающие на слезу истории.""",
        alias='nakige'
    )
    storige, _ = Tag.objects.get_or_create(
        title='сториге',
        description="""Сториге (от англ. "story"&nbsp;&#8211; "история" и ゲ, сокр. от "ゲーム"&nbsp;&#8211; "игра")
                        &nbsp;&#8211; подвид визуальных новелл, в которых основной упор делается на сюжет.""",
        alias='storige'
    )
    eroge, _ = Tag.objects.get_or_create(
        title='эроге (18+)',
        description="""Эроге (エロゲ, от англ. "Erotic game")&nbsp;&#8211; японская порнографическая игра. От обычной 
                        визуальной новеллы отличается наличием в ней 
                        порнографических материалов, не предназначенных для несовершеннолетних.""",
        alias='eroge'
    )
    all_18, _ = Tag.objects.get_or_create(
        title='(18+/all)',
        alias='all_18'
    )
    all_age, _ = Tag.objects.get_or_create(
        title='для всех возрастов (all)',
        alias='all-age'
    )
    chunige, _ = Tag.objects.get_or_create(
        title='чуниге',
        description="""Чуниге (от "中二病" ("синдром восьмиклассника") и "ゲーム" ("игра"))&nbsp;&#8211; подвид 
                        визуальных новелл, в которых одними из основополагающих образующих сюжета являются пафосные 
                        бои, геройская тематика, превозмогания, магия и суперспособности.""",
        alias='chunige'
    )
    true_end, _ = Tag.objects.get_or_create(
        title='есть истинная концовка',
        alias='true-end'
    )
    adv, _ = Tag.objects.get_or_create(
        title='ADV',
        description="""ADV&nbsp;&#8211; вид визуальных новелл, в котором текстовая часть располагается в небольшом 
                        окошке в нижней части экрана. Самый распространённый вид визуальных новелл.""",
        alias='ADV'
    )
    cinetic_novell, _ = Tag.objects.get_or_create(
        title='кинетическая новелла',
        description="""Вид визуальных новелл, в которых полностью отсутствуют ветвления и влияние читателя на сюжет.""",
        alias='kinetic-novel'
    )
    NVL, _ = Tag.objects.get_or_create(
        title='NVL',
        description='Обозначение для новелл, в которых текстовая панель занимает большую часть экрана.',
        alias='NVL'
    )
    ucuge, _ = Tag.objects.get_or_create(
        title='уцуге',
        description="""Уцуге (яп. 鬱ゲー) дословно означает "депрессивная игра". Как и следует из названия, 
                        целью таких игр является ввести человека в угнетённое, подавленное состояние. Для их сюжетов 
                        характерно наличие различных безвыходных и тяжёлых ситуаций без какой-либо надежды на улучшение.
                         В отличие от накиге, где зачастую присутствуют "хорошие" концовки, в уцуге история обречена 
                         на несчастливый финал.""",
        alias='ucuge'
    )
    guro, _ = Tag.objects.get_or_create(
        title='гуро',
        description="""Гуро (Erotic Grotesque, Guro)&nbsp;&#8211; характеризуется наличием сцен, вызывающих отвращение 
                        у большинства людей,&nbsp;&#8211; странных, абсурдных и выходящих за рамки привычного. 
                        Обычно это эротические сцены с расчленёнными или выпотрошенными телами, кровопролитие, 
                        каннибализм, отрезание конечностей, извращённые убийства, некрофилия, пластические операции.""",
        alias='guro'
    )
    madness, _ = Tag.objects.get_or_create(
        title='безумие',
        alias='madness'
    )
    magic, _ = Tag.objects.get_or_create(
        title='магия',
        alias='magic'
    )
    despair, _ = Tag.objects.get_or_create(
        title='отчаяние',
        alias='despair'
    )
    moege, _ = Tag.objects.get_or_create(
        title='моэге',
        description="""Моэге (萌えゲー, moege)&nbsp;&#8211; визуальные новеллы или эроге с большим содержанием 
                        <a href="https://ru.wikipedia.org/wiki/%D0%9C%D0%BE%D1%8D">моэ</a>-контента. Для игр данного 
                        жанра характерны простые и "лёгкие" сюжеты, приятное визуальное и звуковое сопровождение, а 
                        также большое наличие стереотипных персонажей.""",
        alias='moege'
    )
    kiarage, _ = Tag.objects.get_or_create(
        title='кяраге',
        decription="""От "character" и "game". Вид визуальных новелл, в которых акцент делается на взаимоотношениях 
                        персонажей. Часто пересекается с моэге.""",
        alias='kiarage'
    )
    stable_game_order, _ = Tag.objects.get_or_create(
        title='неизменяемый порядок прохождения',
        description="""Определённые руты (сюжетные ветки) игры открываются только после прочтения других.""",
        alias='stable-game-order'
    )
    voice_novel, _ = Tag.objects.get_or_create(
        title='звуковая новелла',
        description="""Та же кинетическая новелла, но с большим упором на звуковое сопровождение. Зачастую 
                        представители жанра имеют весьма слабую графическую составляющую, 
                        либо не имеют таковой вовсе.""",
        alias='voice-novel'
    )
    denpa, _ = Tag.objects.get_or_create(
        title='денпа',
        description="""В таких новеллах герои, которые до поры вели себя нормально, вдруг начинают вести себя 
                        неестественным образом, словно на них напало помешательство. Главный герой не всегда 
                        является исключением.""",
        alias='denpa'
    )
    philosophy, _ = Tag.objects.get_or_create(
        title='философия',
        alias='philosophy'
    )
    linear_plot, _ = Tag.objects.get_or_create(
        title='линейный сюжет',
        description="""Игра содержит целиком линейный сюжет, и привычные для визуальных новелл руты (сюжетные арки) 
                        отсутствуют. Это не значит, что в новелле вообще не может быть выборов, но, если есть, они не 
                        оказывают большого воздействия на сюжет.""",
        alias='linear-plot'
    )
    steampunk, _ = Tag.objects.get_or_create(
        title='стимпанк',
        alias='steampunk'
    )
    cyberpunk, _ = Tag.objects.get_or_create(
        title='киберпанк',
        alias='cyberpunk'
    )
    SRPG, _ = Tag.objects.get_or_create(
        title='SRPG',
        description="""Strategy Role-playing game""",
        alias='SRPG'
    )
    nukige, _ = Tag.objects.get_or_create(
        title='нукиге',
        description="""Подвид визуальных новелл, в которых основной упор делается на хентайную составляющую.""",
        alias='nukige'
    )


def add_staff_roles(apps, schema_editor):
    StaffRole = apps.get_model('cinfo', 'StaffRole')
    screenwriter, _ = StaffRole.objects.get_or_create(title='сценарист')
    composer, _ = StaffRole.objects.get_or_create(title='композитор')
    painter, _ = StaffRole.objects.get_or_create(title='художник')
    chardiz, _ = StaffRole.objects.get_or_create(title='чардиз')


def add_studios(apps, schema_editor):
    Studio = apps.get_model('cinfo', 'Studio')
    visual_atrskey, _ = Studio.objects.get_or_create(
        title='Visual Art\'s/Key',
        description="""Студия, основанная выходцами компании <i>Tactics</i>: Маэдой Дзюном, Орито Синдзи и Хиноуэ 
                        Итару,&nbsp;&#8211; и продолжившая развитие жанра <i>накиге</i>, благодаря которому стала 
                        одной из самых значимых студий ВН.""",
        alias='visual-atrskey'
    )
    le_chocolat, _ = Studio.objects.get_or_create(
        title='Le.Chocolat',
        alias='le-chocolat'
    )
    liar_soft, _ = Studio.objects.get_or_create(
        title='Liar-soft',
        description="""Liar-soft (ライアーソフト)&nbsp;&#8211; японский разработчик эроге, дебютировавший в 1999 году с 
                        игрой "Cho~Ita ~Subarashiki Chounouryoku Jinsei~". Студия стала известна благодаря работам 
                        сценариста Хошизоры Метеора ("Кусарихиме", "Forest", "Seven-Bridge"), в последствии снискала 
                        славу за серию "What a..." от сценариста Сакурай Хикару. Отличительной чертой игр компании 
                        можно отметить необычную подачу сюжета и особый графический стиль. Ныне компания продолжает 
                        выпускать игры, а также мангу, ранобе и сборники иллюстраций.""",
        alias='liar-soft'
    )
    akabei_soft2, _ = Studio.objects.get_or_create(
        title='Akabei Soft2',
        description="""Akabei Soft2 (あかべぇそふとつぅ)&nbsp;&#8211; один из самых крупных японских разработчиков эроге, 
                        выросший из додзинси-кружка Akabei Soft. Компания выпускает множество эроге в самых разных 
                        жанрах, самые известные из её игр&nbsp;&#8211; серия "Sharin no Kuni" и "G-senjou no Maou".""",
        alias='akabei-soft2'
    )
    trumple, _ = Studio.objects.get_or_create(
        title='Trumple',
        description="""Trumple&nbsp;&#8211; японская компания, разрабатывающая эроге, основанная выходцами из 
                        обанкротившейся компании Abhar. Выпустив свою единственную эроге, 
                        "Ushinawareta Mirai o Motomete", компания изменила название на Polarstar.""",
        alias='trumple'
    )
    nitroplus, _ = Studio.objects.get_or_create(
        title='Nitroplus',
        description="""Nitroplus (ニトロプラス, Nitro+)&nbsp;&#8211; японский разработчик эроге и визуальных новелл. 
                        Их первый же проект, "Phantom of Inferno", за авторством ныне именитого Уробучи Гена принёс 
                        им славу и почёт. Игры этой студии отличает наличие мрачных и хорошо проработанных сюжетов.""",
        alias='nitroplus'
    )
    shiba_satomi, _ = Studio.objects.get_or_create(
        title='Shiba Satomi',
        description="""Индивидуальный разработчик ВН. Под крылом Arc System Works выпустил True Remembrance 
                        ("Истина Памяти").""",
        alias='shiba-satomi'
    )
    games_5bp, _ = Studio.objects.get_or_create(
        title='5pb. Games',
        description="""5pb. Games&nbsp;&#8211; японский разработчик игр и визуальных новелл, стоящий под началом
                        крупного издателя игр и аниме-музыки 5pb. Был образован в 2006 году выходцами из компании KID. 
                        Наиболее известные игры: "Chaos;Head", "Steins;Gate", "Psycho-Pass".""",
        alias='games-5bp'
    )
    expansion_07, _ = Studio.objects.get_or_create(
        title='07th Expansion',
        description="""07th Expansion&nbsp;&#8211; японский додзинси-кружок, специализирующийся на создании 
                        визуальных новелл. Известность им принесла эроге "Higurashi no Naku Koro ni" за авторством 
                        Ryuukishi07, а закрепили они её игрой "Umineko no Naku Koro ni". На данный момент 
                        является крупной компанией, продолжающей разрабатывать и выпускать эроге.""",
        alias='expansion_07'
    )
    kid, _ = Studio.objects.get_or_create(
        title='KID',
        description="""KID&nbsp;&#8211; крупная японская компания второй половины 90-х, начала 00-х годов, 
                        специализировавшаяся на разработке и портировании визуальных новелл и игр. В 2006 году 
                        объявили о банкротстве, но были подобраны компанией CyberFront. Знаменитые игры: "Ever17 
                        -The Out of Infinity-", "Remember11 -The Age of Infinity-".""",
        alias='KID'
    )
    type_moon, _ = Studio.objects.get_or_create(
        title='Type-Moon',
        description="""Одна из самых известных студий ВН, Type-Moon выросла из додзинси-кружка, основанного Киноко
                        Насу (сценарист) и Такэучи Такаши (писатель). Прославились после выпуска ВН "Tsukihime", 
                        однако мировую известность им принесла их следующая новелла&nbsp;&#8211; "Fate/Stay Night". 
                        Эти произведения, а также их первая работа, ранобе "Kara no Kyoukai", происходят в единой 
                        вселенной.""",
        alias='type-moon'
    )
    stage_nana, _ = Studio.objects.get_or_create(
        title='Stage-nana',
        alias='stage-nana'
    )
    flying_shine, _ = Studio.objects.get_or_create(
        title='FlyingShine',
        alias='flying-shine'
    )
    innocent_grey, _ = Studio.objects.get_or_create(
        title='Innocent Grey',
        description="""Innocent Grey (inogrey)&nbsp;&#8211; основанная в 2005 году художницей Мики Сугиной студия, 
                        известная за свои исторические эроге в жанре детектив ("Cartagra", серия "Kara no Shoujo"). 
                        До недавнего времени отличительной особенностью игр было большое количество чрезмерной
                         жестокости и ангста, но выход первой части игры "Flowers" положил этому конец.""",
        alias='innocent-grey'
    )
    d_o, _ = Studio.objects.get_or_create(
        title='D.O.',
        alias='do'
    )
    willplus_and_ruf, _ = Studio.objects.get_or_create(
        title='WillPlus & rúf',
        alias='willplus-and-ruf'
    )
    leaf, _ = Studio.objects.get_or_create(
        title='Leaf',
        description="""Leaf&nbsp;&#8211; японская студия, разрабатывающая визуальные новеллы и эроге под издательством 
                        медиакомпании AQUAPLUS. В начале своей деятельности в конце 90-х, в начале 2000-х годов прямо 
                        конкурировала с известной ныне студией Key. Отличительными играми того периода можно назвать 
                        Kizuato, To Heart, White Album и Utawarerumono. В последние года студия занята развитием 
                        своих самых успешных проектов: White Album и Utawarerumono.""",
        alias='leaf'
    )
    novectacle, _ = Studio.objects.get_or_create(
        title='Novectacle',
        alias='novectacle'
    )
    alice_soft, _ = Studio.objects.get_or_create(
        title='Alice Soft',
        alias='alice-soft'
    )
    keroq, _ = Studio.objects.get_or_create(
        title='KeroQ',
        alias='keroq'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('cinfo', '0008_add_alias_field'),
    ]

    operations = [
        migrations.RunPython(add_genres, add_tags, add_staff_roles, add_studios),
    ]