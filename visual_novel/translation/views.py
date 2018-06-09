import arrow
import pytz

from django.conf import settings
from django.shortcuts import render
from django.http import Http404
from django.utils.decorators import decorator_from_middleware

from core.middlewares import IsAuthenticatedMiddleware
from translation.middlewares import HasPermissionToEditVNMiddleware

from .models import TranslationItem, TranslationStatisticsChapter, TranslationSubscription, TranslationBetaLink
from .utils import statistics_name, select_like_statistics_name


@decorator_from_middleware(IsAuthenticatedMiddleware)
@decorator_from_middleware(HasPermissionToEditVNMiddleware)
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

    context['pictures_statistics'] = statistics.pictures_statistics
    context['technical_statistics'] = statistics.technical_statistics
    context['comment'] = statistics.comment
    context['last_update'] = statistics.last_update.isoformat()
    context['alias'] = vn_alias
    context['translation_item'] = translation_item.id

    return render(request, 'translation/edit.html', context)


def all_translations(request):
    all_translations = TranslationItem.objects.filter(
        is_published=True,
        visual_novel__is_published=True
    ).order_by('visual_novel__title')

    context = dict()
    context['novels'] = list()

    for translation in all_translations:
        visual_novel = translation.visual_novel
        statistics = TranslationStatisticsChapter.objects.get(
            tree_id=translation.statistics.tree_id,
            lft=1
        )

        user_timezone = pytz.timezone(settings.DEFAULT_TIME_ZONE) \
            if not hasattr(request.user, 'profile') \
            else request.user.profile.timezone

        last_update = arrow.get((statistics.last_update).replace(tzinfo=pytz.utc)).to(user_timezone).datetime

        total = statistics.total_rows if statistics.total_rows>0 else 1

        context['novels'].append({
            'title': visual_novel.title,
            'total_rows': statistics.total_rows,
            'translated': statistics.translated,
            'edited_first_pass': statistics.edited_first_pass,
            'edited_second_pass': statistics.edited_second_pass,
            'last_update': last_update.__str__()[:19],
            'alias': visual_novel.alias,
            'translated_perc': "{0:.2f}%".format(statistics.translated / total * 100.0),
            'edited_first_pass_perc': "{0:.2f}%".format(statistics.edited_first_pass / total * 100.0),
            'edited_second_pass_perc': "{0:.2f}%".format(statistics.edited_second_pass / total * 100.0)
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
    context['translated_perc'] = "{0:.2f}%".format(base_node.translated / base_node.total_rows * 100.0)
    context['edited_first_pass_perc'] = "{0:.2f}%".format(base_node.edited_first_pass / base_node.total_rows * 100.0)
    context['edited_second_pass_perc'] = "{0:.2f}%".format(base_node.edited_second_pass / base_node.total_rows * 100.0)

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
