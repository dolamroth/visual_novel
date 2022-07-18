import os

from django.shortcuts import render
from django.conf import settings
from django.http import Http404, HttpResponseRedirect

from vn_core.models import VNStaff

from core.utils import printable_russian_date

from .models import ChartItem, ChartItemToUser, ChartRating

from .utils import ChartViewContext


def add_favorite_chart(request, vn_title: str):
    chart_item = ChartItem.objects.get(visual_novel__title=vn_title)
    user, _ = ChartItemToUser.objects.get_or_create(user=request.user, chart_item=chart_item)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def remove_favorite_chart(request, vn_title: str):
    ChartItemToUser.objects.filter(user__id=request.user.id, chart_item__visual_novel__title=vn_title).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def register_rating(request, vn_title: str, rating: int):
    chart_item = ChartItem.objects.get(visual_novel__title=vn_title)
    try:
        user = ChartRating.objects.get(user=request.user, chart_item=chart_item)
        user.rating = rating
        user.save()
    except ChartRating.DoesNotExist:
        ChartRating.objects.create(user=request.user, chart_item=chart_item, rating=rating)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def chart_index_page(
        request,
        genre_alias=None, tag_alias=None, studio_alias=None, staff_alias=None, duration_alias=None,
        translator_alias=None
    ):
    context = ChartViewContext(
        request,
        genre_alias=genre_alias, tag_alias=tag_alias, studio_alias=studio_alias, staff_alias=staff_alias,
        duration_alias=duration_alias, translator_alias=translator_alias, title='Чарт визуальных новелл', additional_breadcumb='Чарт'
    ).get_context()
    return render(request, 'chart/index.html', context)


def chart_favorite_page(
        request,
        genre_alias=None, tag_alias=None, studio_alias=None, staff_alias=None, duration_alias=None,
        translator_alias=None
    ):
    context = ChartViewContext(
        request,
        genre_alias=genre_alias, tag_alias=tag_alias, studio_alias=studio_alias, staff_alias=staff_alias,
        duration_alias=duration_alias, translator_alias=translator_alias, title='Избранное', additional_breadcumb='Избранное'
    ).get_context()
    return render(request, 'chart/favorites.html', context)


def chart_page(request, vn_alias):
    vn_context = dict()
    try:
        chart_item = ChartItem.objects.get(
            is_published=True, visual_novel__is_published=True, visual_novel__alias=vn_alias
        )
    except ChartItem.DoesNotExist:
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
    vn_context['vndb_mark'] = visual_novel.get_rate()
    vn_context['vndb_popularity'] = visual_novel.get_popularity()
    vn_context['vndb_vote_count'] = visual_novel.vote_count

    vn_context['description'] = visual_novel.description
    vn_context['has_description'] = not not vn_context['description']

    vn_context['comment'] = chart_item.comment
    vn_context['has_comment'] = not not vn_context['comment']

    keywords = list()

    # Genres list
    vn_context['genres'] = list()
    for genre in visual_novel.vngenre_set.filter(genre__is_published=True).order_by('-weight'):
        vn_context['genres'].append({
            'title': genre.genre.title,
            'description': genre.genre.description,
            'link': f'genre/{genre.genre.alias}',
            'has_description': not not genre.genre.description,
            'alias': genre.genre.alias
        })
        keywords.append(genre.genre.title)
    vn_context['has_genres'] = (len(vn_context['genres']) > 0)

    # Studios list
    vn_context['studios'] = list()
    for studio in visual_novel.vnstudio_set.filter(studio__is_published=True).order_by('-weight'):
        vn_context['studios'].append({
            'title': studio.studio.title,
            'description': studio.studio.description,
            'link': 'studio',
            'has_description': not not studio.studio.description,
            'alias': studio.studio.alias
        })
        keywords.append(studio.studio.title)
    vn_context['has_studios'] = (len(vn_context['studios']) > 0)

    # Tags list
    vn_context['tags'] = list()
    for tag in visual_novel.vntag_set.filter(tag__is_published=True).order_by('-weight'):
        vn_context['tags'].append({
            'title': tag.tag.title,
            'description': tag.tag.description.replace('\"', '\''),
            'link': 'tags',
            'has_description': not not tag.tag.description,
            'alias': tag.tag.alias
        })
        keywords.append(tag.tag.title)
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
            'link': 'staff',
            'description': staff.description,
            'has_description': not not staff.description,
            'roles': roles,
            'alias': staff.alias
        })
        keywords.append(staff.title)
    vn_context['has_staffs'] = (len(vn_context['staffs']) > 0)

    # Translators list
    vn_context['translators'] = list()
    for translator in chart_item.chartitemtranslator_set.filter(translator__is_published=True):
        vn_context['translators'].append({
            'title': translator.translator.title,
            'description': translator.translator.description.replace('\"', '\''),
            'link': 'translator',
            'has_description': not not translator.translator.description,
            'alias': translator.translator.alias,
            'language': translator.language.title,
            'url': translator.translator.url or None
        })
        keywords.append(translator.translator.title)
    vn_context['has_translators'] = (len(vn_context['translators']) > 0)

    vn_context['keywords'] = ", ".join(keywords)

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
