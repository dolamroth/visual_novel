import arrow
import pytz

from django.conf import settings
from django.shortcuts import render
from django.http import Http404

from core.middlewares import IsAuthenticatedMiddleware
from translation.middlewares import HasPermissionToEditVNMiddleware

from .choices import TRANSLATION_ITEMS_STATUSES
from .models import TranslationItem, TranslationStatisticsChapter, TranslationSubscription, TranslationBetaLink
from .utils import statistics_name, select_like_statistics_name, get_status_tuple_for_translation_item


@IsAuthenticatedMiddleware
@HasPermissionToEditVNMiddleware
def edit_statistics(request, vn_alias):

    try:
        translation_item = TranslationItem.objects.get(
            visual_novel__alias=vn_alias,
            is_published=True,
            visual_novel__is_published=True
        )
    except TranslationItem.DoesNotExist:
        raise Http404

    context = dict()

    visual_novel = translation_item.visual_novel
    statistics = translation_item.statistics

    context['title'] = visual_novel.title
    context['username'] = request.user.username

    context['statistics'] = list()
    context['move_to_list'] = list()
    for item in TranslationStatisticsChapter.objects.filter(
        tree_id=statistics.tree_id
    ).order_by('lft'):
        parent = item.parent
        context['statistics'].append({
            'title': item.title.replace('"', '\''),
            'script_title': item.script_title.replace('"', '\''),
            'parent_id': 0 if not parent else parent.id,
            'name': statistics_name(item).replace('"', '\''),
            'is_editable': not not parent,
            'total_rows': item.total_rows,
            'translated': item.translated,
            'edited_first_pass': item.edited_first_pass,
            'edited_second_pass': item.edited_second_pass,
            'is_chapter': item.is_chapter,
            'translation_item': translation_item.id,
            'id': item.id
        })
        context['move_to_list'].append({
            'id': item.id,
            'title': select_like_statistics_name(item)
        })

    context['download_links'] = [
        d for d in TranslationBetaLink.objects.filter(
            is_published=True,
            translation_item=translation_item
        ).values('id', 'title', 'url', 'comment', 'approved', 'rejected')
    ]

    context['statuses'] = list()
    for translation_status in TRANSLATION_ITEMS_STATUSES:
        if translation_status[3]:
            context['statuses'].append({
                'key': translation_status[0],
                'name': translation_status[1],
                'style': translation_status[2],
                'mailing_inform': translation_status[4],
                'description': translation_status[5]
            })

    try:
        status = [d for d in translation_item.status if d[1]][0][0]
        status_tuple = [d for d in TRANSLATION_ITEMS_STATUSES if d[0] == status][0]
        status_key = status_tuple[0]
        status_name = status_tuple[1]
        status_bootstrap_tr_style = status_tuple[2]
    except KeyError:
        status_key = 'unknown'
        status_name = 'Неизвестно'
        status_bootstrap_tr_style = 'warning'
    context['status_key'] = status_key
    context['status_name'] = status_name
    context['status_style'] = status_bootstrap_tr_style

    context['pictures_statistics'] = statistics.pictures_statistics
    context['technical_statistics'] = statistics.technical_statistics
    context['comment'] = statistics.comment
    context['last_update'] = statistics.last_update.isoformat()
    context['alias'] = vn_alias
    context['translation_item'] = translation_item.id

    return render(request, 'translation/edit.html', context)


def all_translations(request, **kwargs):
    all_translations = TranslationItem.objects.filter(
        is_published=True,
        visual_novel__is_published=True
    ).order_by('visual_novel__title')

    context = dict()
    context['novels'] = list()
    context['additional_breadcumb'] = '&nbsp;&#47; Список ведущихся переводов'
    translation_breadcumb_with_link = '&nbsp;&#47; <a href="/translation/all">Список ведущихся переводов</a>&nbsp;&#47; Статус:&nbsp;'

    if 'status_key' in kwargs.keys():
        all_status_keys = list(TranslationItem.status)
        k = 1
        for key in all_status_keys:
            if key == kwargs['status_key']:
                break
            k *= 2
        all_translations = all_translations.filter(status=k)
        context['additional_breadcumb'] = translation_breadcumb_with_link \
            + [d for d in TRANSLATION_ITEMS_STATUSES if d[0] == kwargs['status_key']][0][1]

    context['statuses'] = list()
    for translation_status in TRANSLATION_ITEMS_STATUSES:
        if translation_status[3]:
            context['statuses'].append({
                'key': translation_status[0],
                'name': translation_status[1],
                'style': translation_status[2],
                'mailing_inform': translation_status[4],
                'description': translation_status[5]
            })

    for translation in all_translations:
        visual_novel = translation.visual_novel
        statistics = TranslationStatisticsChapter.objects.get(
            tree_id=translation.statistics.tree_id,
            lft=1
        )

        user_timezone = pytz.timezone(settings.DEFAULT_TIME_ZONE) \
            if not hasattr(request.user, 'profile') \
            else request.user.profile.timezone

        last_update = arrow.get((translation.statistics.last_update)
                                .replace(tzinfo=pytz.utc)).to(user_timezone).datetime

        total = statistics.total_rows if statistics.total_rows > 0 else 1

        try:
            status_tuple = get_status_tuple_for_translation_item(translation)
            status_name = status_tuple[1]
            status_bootstrap_tr_style = status_tuple[2]
        except KeyError:
            continue

        context['novels'].append({
            'title': visual_novel.title,
            'total_rows': statistics.total_rows,
            'translated': statistics.translated,
            'edited_first_pass': statistics.edited_first_pass,
            'edited_second_pass': statistics.edited_second_pass,
            'last_update': last_update.strftime("%Y-%m-%d %H:%M"),
            'alias': visual_novel.alias,
            'translated_perc': "{0:.2f}%".format(statistics.translated / total * 100.0),
            'edited_first_pass_perc': "{0:.2f}%".format(statistics.edited_first_pass / total * 100.0),
            'edited_second_pass_perc': "{0:.2f}%".format(statistics.edited_second_pass / total * 100.0),
            'status_name': status_name,
            'status_style': status_bootstrap_tr_style
        })

    return render(request, 'translation/all.html', context)


def translation_item_view(request, vn_alias):
    try:
        translation = TranslationItem.objects.get(
            is_published=True,
            visual_novel__is_published=True,
            visual_novel__alias=vn_alias
        )
    except TranslationItem.DoesNotExist:
        return render(request, 'translation/item_does_not_exist.html')

    context = dict()

    visual_novel = translation.visual_novel

    context['title'] = visual_novel.title
    context['alias'] = visual_novel.alias

    try:
        status_tuple = get_status_tuple_for_translation_item(translation)
        status_name = status_tuple[1]
        status_bootstrap_tr_style = status_tuple[2]
    except KeyError:
        status_name = 'Неизвестно'
        status_bootstrap_tr_style = 'warning'
    context['status_name'] = status_name
    context['status_style'] = status_bootstrap_tr_style

    translator = translation.translator
    context['translator'] = None
    context['translator_link'] = None
    if translator:
        context['translator'] = translator.title
        if translator.url:
            if translator.url.startswith("club") and translator.url[4:].isdigit():
                context['translator_link'] = "https://vk.com/" + translator.url
            elif translator.url.startswith("https://"):
                context['translator_link'] = translator.url

    context['items'] = list()

    statistics = translation.statistics

    context['pictures_statistics'] = statistics.pictures_statistics
    context['technical_statistics'] = statistics.technical_statistics
    context['comment'] = statistics.comment

    context['has_pictures_statistics'] = not not statistics.pictures_statistics
    context['has_technical_statistics'] = not not statistics.technical_statistics
    context['has_comment'] = not not statistics.comment

    base_node = TranslationStatisticsChapter.objects.get(
        tree_id=statistics.tree_id,
        lft=1
    )

    context['total_rows'] = base_node.total_rows
    context['translated'] = base_node.translated
    context['edited_first_pass'] = base_node.edited_first_pass
    context['edited_second_pass'] = base_node.edited_second_pass

    total = context['total_rows'] if context['total_rows']>0 else 1

    context['translated_perc'] = "{0:.2f}%".format(base_node.translated / total * 100.0)
    context['edited_first_pass_perc'] = "{0:.2f}%".format(base_node.edited_first_pass / total * 100.0)
    context['edited_second_pass_perc'] = "{0:.2f}%".format(base_node.edited_second_pass / total * 100.0)

    context['download_links'] = [
        d for d in TranslationBetaLink.objects.filter(
            is_published=True,
            translation_item=translation,
            approved=True,
            rejected=False
        ).values('id', 'title', 'url', 'comment', 'approved', 'rejected')
    ]
    context['has_download_links'] = (len(context['download_links']) > 0)

    all_items = TranslationStatisticsChapter.objects.filter(
        tree_id=statistics.tree_id,
        lft__gt=1
    ).order_by('lft')

    for item in all_items:
        context['items'].append({
            'name': statistics_name(item, base_level=1, script=False).replace('"', '\''),
            'total_rows': item.total_rows,
            'translated': item.translated,
            'edited_first_pass': item.edited_first_pass,
            'edited_second_pass': item.edited_second_pass,
            'is_chapter': item.is_chapter
        })

    context['is_subscribed'] = request.user.is_authenticated  \
        and TranslationSubscription.objects.filter(profile=request.user.profile, translation=translation).exists()

    return render(request, 'translation/item.html', context)
