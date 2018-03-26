from django.shortcuts import render
from django.conf import settings
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
    for item in TranslationStatisticsChapter.objects.filter(
        tree_id=statistics.tree_id
    ).order_by('lft'):
        parent = item.parent
        context['statistics'].append({
            'title': item.title,
            'script_title': item.script_title,
            'parent_id': 0 if not parent else parent.id,
            'name': item.statistics_name(),
            'is_editable': not not parent,
            'total_rows': '{:18}: {}'.format("Всего строк", item.total_rows).replace(' ', '&nbsp;'),
            'translated': '{:18}: {}'.format("Перевод", item.translated).replace(' ', '&nbsp;'),
            'edited_first_pass': '{:18}: {}'.format("Редактура 1", item.edited_first_pass).replace(' ', '&nbsp;'),
            'edited_second_pass': '{:18}: {}'.format("Редактура 2", item.edited_second_pass).replace(' ', '&nbsp;')
        })

    context['pictures_statistics'] = statistics.pictures_statistics
    context['technical_statistics'] = statistics.technical_statistics
    context['comment'] = statistics.comment
    context['last_update'] = statistics.last_update.isoformat()

    return render(request, 'translation/edit.html', context)
