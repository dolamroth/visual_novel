import os

from django.shortcuts import render
from django.conf import settings
from django.http import Http404

from vn_core.models import VNGenre, VNTag, VNStudio, VNStaff
from cinfo.models import Genre, Tag, Studio, Staff, Longevity
from core.utils import printable_russian_date

from .models import ChartItem


def chart_index_page(
        request,
        genre_alias=None, tag_alias=None, studio_alias=None, staff_alias=None, duration_alias=None
    ):
    context = dict()
    context['additional_breadcumb'] = '&nbsp;&#47;&nbsp;Чарт'
    chart_breadcumb_with_link = '&nbsp;&#47;&nbsp;<a href="/chart/">Чарт</a>&nbsp;&#47;&nbsp;'

    rows = list()
    max_vn_by_row = settings.CHART_NUMBER_OF_VN_IN_ROW

    all_chart_items = ChartItem.objects.filter(is_published=True, visual_novel__is_published=True)

    context['all_genres'] = Genre.objects.filter(is_published=True).order_by('title').values()
    context['all_tags'] = Tag.objects.filter(is_published=True).order_by('title').values()
    context['all_durations'] = Longevity.objects.filter(is_published=True).order_by('max_length').values()
    context['all_studios'] = Studio.objects.filter(is_published=True).order_by('title').values()
    context['all_staff'] = Staff.objects.filter(is_published=True).order_by('title').values()

    # Optional endpoint parameters
    if genre_alias:
        vn_with_genre = VNGenre.objects.filter(genre__alias=genre_alias).values('visual_novel')
        all_chart_items = all_chart_items.filter(visual_novel__in=vn_with_genre)
        try:
            genre = Genre.objects.get(alias=genre_alias)
            context['additional_breadcumb'] = chart_breadcumb_with_link + 'жанр: ' + genre.title
        except Genre.DoesNotExist:
            pass

    if tag_alias:
        vn_with_tag = VNTag.objects.filter(tag__alias=tag_alias).values('visual_novel')
        all_chart_items = all_chart_items.filter(visual_novel__in=vn_with_tag)
        try:
            tag = Tag.objects.get(alias=tag_alias)
            context['additional_breadcumb'] = chart_breadcumb_with_link + 'тэг: ' + tag.title
        except Tag.DoesNotExist:
            pass

    if studio_alias:
        vn_with_studio = VNStudio.objects.filter(studio__alias=studio_alias).values('visual_novel')
        all_chart_items = all_chart_items.filter(visual_novel__in=vn_with_studio)
        try:
            studio = Studio.objects.get(alias=studio_alias)
            context['additional_breadcumb'] = chart_breadcumb_with_link + 'студия: ' + studio.title
        except Studio.DoesNotExist:
            pass

    if staff_alias:
        vn_with_staff = VNStaff.objects.filter(staff__alias=staff_alias).values('visual_novel')
        all_chart_items = all_chart_items.filter(visual_novel__in=vn_with_staff)
        try:
            staff = Staff.objects.get(alias=staff_alias)
            context['additional_breadcumb'] = chart_breadcumb_with_link + 'персона: ' + staff.title
        except Staff.DoesNotExist:
            pass

    if duration_alias:
        all_chart_items = all_chart_items.filter(visual_novel__longevity__alias=duration_alias)
        try:
            duration = Longevity.objects.get(alias=duration_alias)
            context['additional_breadcumb'] = chart_breadcumb_with_link + 'продолжительность: ' + duration.title
        except Longevity.DoesNotExist:
            pass

    # Visual novels are grouped in list in groups of settings.CHART_NUMBER_OF_VN_IN_ROW
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

    if 0 < len(row) < settings.CHART_NUMBER_OF_VN_IN_ROW:
        rows.append(row)

    context['rows'] = rows
    context['no_rows'] = (len(context['rows']) == 0)
    if context['no_rows']:
        context['additional_breadcumb'] = '&nbsp;&#47;&nbsp;<a href="/chart/">Чарт</a>'

    return render(request, 'chart/index.html', context)


def chart_page(request, vn_alias):
    vn_context = dict()
    try:
        chart_item = ChartItem.objects.get(
            is_published=True, visual_novel__is_published=True, visual_novel__alias=vn_alias
        )
    except:
        raise Http404

    visual_novel = chart_item.visual_novel

    vn_context['title'] = visual_novel.title
    vn_context['alternative_title'] = visual_novel.alternative_title
    vn_context['poster_url'] = settings.POSTER_STOPPER_URL if not visual_novel.photo else visual_novel.photo.url
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

    vn_context['description'] = visual_novel.description
    vn_context['has_description'] = not not vn_context['description']

    vn_context['comment'] = chart_item.comment
    vn_context['has_comment'] = not not vn_context['comment']

    # Genres list
    vn_context['genres'] = list()
    for genre in visual_novel.vngenre_set.filter(genre__is_published=True).order_by('-weight'):
        vn_context['genres'].append({
            'title': genre.genre.title,
            'description': genre.genre.description,
            'link': ('/chart/genre' + genre.genre.alias),
            'has_description': not not genre.genre.description,
            'alias': genre.genre.alias
        })
    vn_context['has_genres'] = (len(vn_context['genres']) > 0)

    # Studios list
    vn_context['studios'] = list()
    for studio in visual_novel.vnstudio_set.filter(studio__is_published=True).order_by('-weight'):
        vn_context['studios'].append({
            'title': studio.studio.title,
            'description': studio.studio.description,
            'link': ('/chart/studio' + studio.studio.alias),
            'has_description': not not studio.studio.description,
            'alias': studio.studio.alias
        })
    vn_context['has_studios'] = (len(vn_context['studios']) > 0)

    # Tags list
    vn_context['tags'] = list()
    for tag in visual_novel.vntag_set.filter(tag__is_published=True).order_by('-weight'):
        vn_context['tags'].append({
            'title': tag.tag.title,
            'description': tag.tag.description.replace('\"', '\''),
            'link': ('/chart/tag/' + tag.tag.alias),
            'has_description': not not tag.tag.description,
            'alias': tag.tag.alias
        })
    vn_context['has_tags'] = (len(vn_context['tags']) > 0)

    # Staff list
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
            'link': ('/chart/staff' + staff.alias),
            'description': staff.description,
            'has_description': not not staff.description,
            'roles': roles,
            'alias': staff.alias
        })
    print(vn_context['staffs'])
    vn_context['has_staffs'] = (len(vn_context['staffs']) > 0)

    # Screenshots list
    vn_context['screenshots'] = list()
    vn_screenshots = chart_item.chartitemscreenshot_set.filter(
        is_published=True,
        image__isnull=False,
        miniature__isnull=False
    ).order_by('-order')
    for screenshot in vn_screenshots:
        vn_context['screenshots'].append({
            'title': screenshot.title,
            'image': screenshot.image.url,
            'miniature': screenshot.miniature.url
        })
    vn_context['has_screenshots'] = (len(vn_context['screenshots']) > 0)

    return render(request=request, template_name='chart/item.html', context=vn_context)
