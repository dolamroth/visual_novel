from django.shortcuts import render
from django.http import Http404
from django.utils.decorators import decorator_from_middleware

from core.middlewares import IsAuthenticatedMiddleware
from translation.middlewares import HasPermissionToEditVNMiddleware

from .models import TranslationItem, TranslationStatisticsChapter


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
            'name': item.statistics_name().replace('"', '\''),
            'is_editable': not not parent,
            'total_rows': item.total_rows,
            'translated': item.translated,
            'edited_first_pass': item.edited_first_pass,
            'edited_second_pass': item.edited_second_pass,
            'is_chapter': item.is_chapter,
            'translation_item': translation_item.id,
            'id': item.id
        })
        if item.lft > 1:
            context['move_to_list'].append({
                'id': item.id,
                'title': item.select_like_statistics_name()
            })

    context['pictures_statistics'] = statistics.pictures_statistics
    context['technical_statistics'] = statistics.technical_statistics
    context['comment'] = statistics.comment
    context['last_update'] = statistics.last_update.isoformat()
    context['alias'] = vn_alias

    return render(request, 'translation/edit.html', context)
