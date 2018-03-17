import os

from django.shortcuts import render, render_to_response
from django.conf import settings

from .models import ChartItem
from vn_core.models import VNStaff


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

    return render(request, 'chart/index.html', context)


def chart_page(request, vn_alias):
    vn_context = dict()
    chart_item = ChartItem.objects.get(is_published=True, visual_novel__is_published=True, visual_novel__alias=vn_alias)
    visual_novel = chart_item.visual_novel

    vn_context['title'] = visual_novel.title
    vn_context['alternative_title'] = visual_novel.alternative_title
    vn_context['poster_url'] = settings.POSTER_STOPPER_URL if not visual_novel.photo else visual_novel.photo.url
    vn_context['description'] = visual_novel.description
    vn_context['vndb_id'] = visual_novel.vndb_id
    vn_context['chart_link'] = os.path.join('/chart/', visual_novel.alias)
    vn_context['steam_link'] = visual_novel.steam_link
    vn_context['longevity'] = visual_novel.longevity.__str__()
    vn_context['date_of_release'] = visual_novel.date_of_release

    vn_context['genres'] = list()
    for genre in visual_novel.vngenre_set.all().order_by('-weight'):
        vn_context['genres'].append({
            'title': genre.genre.title,
            'description': genre.genre.description,
            'link': os.path.join('/chart/', 'genre', genre.genre.alias)
        })

    vn_context['studios'] = list()
    for studio in visual_novel.vnstudio_set.all().order_by('-weight'):
        vn_context['studios'].append({
            'title': studio.studio.title,
            'description': studio.studio.description,
            'link': os.path.join('/chart/', 'studio', studio.studio.alias)
        })

    vn_context['tags'] = list()
    for tag in visual_novel.vntag_set.all().order_by('-weight'):
        vn_context['tags'].append({
            'title': tag.tag.title,
            'description': tag.tag.description,
            'link': os.path.join('/chart/', 'tag', tag.tag.alias)
        })

    vn_context['staffs'] = list()
    staffs_clear = list()
    for staff in visual_novel.vnstaff_set.all().order_by('-weight'):
        if staff.staff not in staffs_clear:
            staffs_clear.append(staff.staff)
    for staff in staffs_clear:
        vnstaffs = VNStaff.objects.filter(staff=staff).distinct('role__title')
        roles = [vnstaffs[i].role for i in range(len(vnstaffs))]
        vn_context['staffs'].append({
            'title': staff.title,
            'link': os.path.join('/chart/', 'staff', staff.alias),
            'roles': roles
        })

    return render(request=request, template_name='chart/item.html', context=vn_context)
