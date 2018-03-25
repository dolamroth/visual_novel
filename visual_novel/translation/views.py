from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from django.utils.decorators import decorator_from_middleware

from core.middlewares import IsAuthenticatedMiddleware

from .models import TranslationItem, TranslationStatisticsChapter


@decorator_from_middleware(IsAuthenticatedMiddleware)
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

    context['title'] = visual_novel.title
    context['username'] = request.user.username

    context['statistics'] = list()
    for item in TranslationStatisticsChapter.objects.filter(
        tree_id=translation_item.statistics.tree_id
    ).order_by('lft'):
        context['statistics'].append({
            'title': item.title,
            'script_title': item.script_title,
            'parent_id': 0 if not item.parent else item.parent.id,
            'name': item.statistics_name()
        })

    return render(request, 'translation/edit.html', context)
