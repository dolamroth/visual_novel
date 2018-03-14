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


class Migration(migrations.Migration):

    dependencies = [
        ('cinfo', '0008_add_alias_field'),
    ]

    operations = [
        migrations.RunPython(add_genres, add_tags, add_staff_roles),
    ]