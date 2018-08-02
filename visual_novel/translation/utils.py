from .choices import TRANSLATION_ITEMS_STATUSES


def statistics_name(translation_item, base_level=0, script=True):
    name = translation_item.script_title if script else translation_item.title
    add = ''
    if translation_item.is_chapter:
        add = 'font-weight: 700;'
    name = '<span style="margin-left:{}em; {}">{}</span>'.format(
        translation_item.get_level() - base_level,
        add,
        name)
    return name


def select_like_statistics_name(translation_item, base_level=0):
    return '---' * (translation_item.get_level() - base_level) + ' ' + str(translation_item.script_title)


def get_status_tuple_for_translation_item(translation_item):
    status = [d for d in translation_item.status if d[1]][0][0]
    status_tuple = [d for d in TRANSLATION_ITEMS_STATUSES if d[0] == status][0]
    return status_tuple
