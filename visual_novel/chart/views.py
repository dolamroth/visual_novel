import os

from django.shortcuts import render
from django.conf import settings

from .models import ChartItem


def chart_index_page(request):
    context = dict()

    rows = list()
    max_vn_by_row = settings.CHART_NUMBER_OF_VN_IN_ROW

    all_chart_items = ChartItem.objects.filter(is_published=True, visual_novel__is_published=True)
    k = 0
    row = list()
    for chart_item in all_chart_items:
        vn_context = dict()

        visual_novel = chart_item.visual_novel

        vn_context['title'] = visual_novel.title
        vn_context['poster_url'] = settings.POSTER_STOPPER_URL if not visual_novel.photo else visual_novel.photo.url
        vn_context['description'] = visual_novel.description
        vn_context['genres'] = list()
        vn_context['vndb_id'] = visual_novel.vndb_id
        vn_context['chart_link'] = os.path.join('/chart/', visual_novel.alias)

        for genre in visual_novel.vngenre_set.all().order_by('-weight'):
            vn_context['genres'].append({
                'title': genre.genre.title,
                'link': os.path.join('/chart/', 'genre', genre.genre.alias)
            })

        vn_context['studios'] = list()
        for studio in visual_novel.vnstudio_set.all().order_by('-weight'):
            vn_context['studios'].append({
                'title': studio.studio.title,
                'link': os.path.join('/chart/', 'studio', studio.studio.alias)
            })

        row.append(vn_context)

        k += 1

        if k % max_vn_by_row == 0:
            rows.append(row)
            row = list()

        if len(row) < settings.CHART_NUMBER_OF_VN_IN_ROW:
            rows.append(row)

    context['rows'] = rows
    print(context)

    return render(request, 'chart/index.html', context)
