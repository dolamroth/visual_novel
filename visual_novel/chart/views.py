import os

from django.shortcuts import render
from django.conf import settings

from vn_core.models import VNStaff
from core.utils import printable_russian_date

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
    vn_context['has_steam'] = not not visual_novel.steam_link
    vn_context['steam_link'] = visual_novel.steam_link or ''
    vn_context['steam_icon'] = settings.STEAM_ICON_URL
    vn_context['longevity'] = visual_novel.longevity.__str__()
    vn_context['longevity_link'] = os.path.join('/chart/', 'duration', visual_novel.longevity.alias)
    vn_context['date_of_release'] = printable_russian_date(visual_novel.date_of_release)
    vn_context['date_of_translation'] = printable_russian_date(chart_item.date_of_translation)
    vn_context['vndb_mark'] = 0 # TODO: fix

    vn_context['genres'] = list()
    for genre in visual_novel.vngenre_set.filter(genre__is_published=True).order_by('-weight'):
        vn_context['genres'].append({
            'title': genre.genre.title,
            'description': genre.genre.description,
            'link': os.path.join('/chart/', 'genre', genre.genre.alias)
        })
    vn_context['has_genres'] = (len(vn_context['genres']) > 0)

    vn_context['studios'] = list()
    for studio in visual_novel.vnstudio_set.filter(studio__is_published=True).order_by('-weight'):
        vn_context['studios'].append({
            'title': studio.studio.title,
            'description': studio.studio.description,
            'link': os.path.join('/chart/', 'studio', studio.studio.alias)
        })
    vn_context['has_studios'] = (len(vn_context['studios']) > 0)

    vn_context['tags'] = list()
    for tag in visual_novel.vntag_set.filter(tag__is_published=True).order_by('-weight'):
        vn_context['tags'].append({
            'title': tag.tag.title,
            'description': tag.tag.description,
            'link': os.path.join('/chart/', 'tag', tag.tag.alias)
        })
    vn_context['has_tags'] = (len(vn_context['tags']) > 0)

    vn_context['staffs'] = list()
    staffs_clear = list()
    for staff in visual_novel.vnstaff_set.filter(staff__is_published=True).order_by('-weight'):
        if staff.staff not in staffs_clear:
            staffs_clear.append(staff.staff)
    for staff in staffs_clear:
        vnstaffs = VNStaff.objects.filter(staff=staff, visual_novel=visual_novel).distinct('role__title')
        roles = [vnstaffs[i].role for i in range(len(vnstaffs))]
        vn_context['staffs'].append({
            'title': staff.title,
            'link': os.path.join('/chart/', 'staff', staff.alias),
            'roles': roles
        })
    vn_context['has_staffs'] = (len(vn_context['staffs']) > 0)

    vn_context['screenshots'] = list()
    vn_screenshots = chart_item.chartitemscreenshot_set.filter(
        is_published=True,
        image__isnull=False,
        miniature__isnull=False
    ).order_by('-order')
    for screenshot in vn_screenshots:
        vn_context['screenshots'].append(
            {
                'title': screenshot.title,
                'image': screenshot.image.url,
                'miniature': screenshot.miniature.url
            }
        )

    return render(request=request, template_name='chart/item.html', context=vn_context)
