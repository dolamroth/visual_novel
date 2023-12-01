import os

from constance import config

from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from django.urls import reverse
from django.core.cache import caches

from vn_core.models import VNGenre, VNTag, VNStudio, VNStaff
from cinfo.models import Genre, Tag, Studio, Staff, Longevity, Translator

from core.utils import printable_russian_date

from .models import ChartItem, ChartItemTranslator
from .serializers import ChartItemListSerializer

cache = caches['default']


def chart_index_page(
        request,
        genre_alias=None, tag_alias=None, studio_alias=None, staff_alias=None, duration_alias=None,
        translator_alias=None
    ):
    context = dict()
    context['additional_breadcumb'] = '&nbsp;&#47; Чарт'
    chart_breadcumb_with_link = '&nbsp;&#47; <a href="/chart/">Чарт</a>&nbsp;&#47; '
    context['additional_description'] = ''

    rows = list()
    max_vn_by_row = settings.CHART_NUMBER_OF_VN_IN_ROW

    # Lazy computed, so no caching here
    all_chart_items = ChartItem.objects\
        .filter(is_published=True, visual_novel__is_published=True)\
        .select_related("visual_novel")

    cache_key = 'chart'

    context['all_genres'] = Genre.objects.filter(is_published=True).order_by('title').values()
    context['all_tags'] = Tag.objects.filter(is_published=True).order_by('title').values()
    context['all_durations'] = Longevity.objects.filter(is_published=True).order_by('max_length').values()
    context['all_studios'] = Studio.objects.filter(is_published=True).order_by('title').values()
    context['all_staff'] = Staff.objects.filter(is_published=True).order_by('title').values()

    # Optional endpoint parameters
    if genre_alias:
        vn_with_genre = VNGenre.objects.filter(genre__alias=genre_alias).values('visual_novel_id')
        all_chart_items = all_chart_items.filter(visual_novel_id__in=vn_with_genre)
        try:
            genre = Genre.objects.get(alias=genre_alias)
            context['additional_breadcumb'] = chart_breadcumb_with_link + 'жанр: ' + genre.title
            cache_key += '_genre_{}'.format(genre_alias)
            if genre.description:
                context['additional_description'] = genre.description
        except Genre.DoesNotExist:
            pass

    if tag_alias:
        vn_with_tag = VNTag.objects.filter(tag__alias=tag_alias).values('visual_novel_id')
        all_chart_items = all_chart_items.filter(visual_novel_id__in=vn_with_tag)
        try:
            tag = Tag.objects.get(alias=tag_alias)
            context['additional_breadcumb'] = chart_breadcumb_with_link + 'тэг: ' + tag.title
            cache_key += '_tag_{}'.format(tag_alias)
            if tag.description:
                context['additional_description'] = tag.description
        except Tag.DoesNotExist:
            pass

    if studio_alias:
        vn_with_studio = VNStudio.objects.filter(studio__alias=studio_alias).values('visual_novel_id')
        all_chart_items = all_chart_items.filter(visual_novel_id__in=vn_with_studio)
        try:
            studio = Studio.objects.get(alias=studio_alias)
            context['additional_breadcumb'] = chart_breadcumb_with_link + 'студия: ' + studio.title
            cache_key += '_studio_{}'.format(studio_alias)
            if studio.description:
                context['additional_description'] = studio.description
        except Studio.DoesNotExist:
            pass

    if staff_alias:
        vn_with_staff = VNStaff.objects.filter(staff__alias=staff_alias).values('visual_novel_id')
        all_chart_items = all_chart_items.filter(visual_novel_id__in=vn_with_staff)
        try:
            staff = Staff.objects.get(alias=staff_alias)
            context['additional_breadcumb'] = chart_breadcumb_with_link + 'персона: ' + staff.title
            cache_key += '_staff_{}'.format(staff_alias)
            if staff.description:
                context['additional_description'] = staff.description
        except Staff.DoesNotExist:
            pass

    if duration_alias:
        all_chart_items = all_chart_items.filter(visual_novel__longevity__alias=duration_alias)
        try:
            duration = Longevity.objects.get(alias=duration_alias)
            cache_key += '_duration_{}'.format(duration_alias)
            context['additional_breadcumb'] = chart_breadcumb_with_link + 'продолжительность: ' + duration.title
        except Longevity.DoesNotExist:
            pass

    if translator_alias:
        translators_ids = ChartItemTranslator.objects.filter(translator__alias=translator_alias)\
            .values_list('item__id', flat=True)
        all_chart_items = all_chart_items.filter(id__in=translators_ids)
        try:
            translator = Translator.objects.get(alias=translator_alias)
            cache_key += '_translator_{}'.format(translator_alias)
            context['additional_breadcumb'] = chart_breadcumb_with_link + 'переводчик: ' + translator.title
            if translator.description or translator.url:
                context['additional_description'] = ''
                translator_description = list()
                if translator.description:
                    translator_description.append(translator.description)
                if translator.url:
                    translator_description.append('<a href="{}">Ссылка на сайт переводчика.</a>'.format(
                        translator.url
                    ))
                context['additional_description'] = '<br /><br />'.join(translator_description)

        except Translator.DoesNotExist:
            pass

    # Sorting list of visual novels
    sort_by = request.GET.get('sort')
    base_sort_by = '-date_of_translation'
    # These two arrays are coordinated in terms of order of elements and corresponding data
    # This array shows all the possible GET parameters for "sort"
    all_sortings = ['-date_of_translation', 'date_of_translation', 'visual_novel__rate', '-visual_novel__rate',
                    '-visual_novel__date_of_release', 'visual_novel__date_of_release', '-visual_novel__title',
                    'visual_novel__title', 'visual_novel__popularity', '-visual_novel__popularity']
    # This array provides alternative sorting for one selected parameter, which is chosen by user,
    # and a title of glyphoicon from Bootstrap
    all_sortings_context_links = [
        ('date_of_translation', 'date_of_translation', 'glyphicon glyphicon-arrow-down'),
        ('date_of_translation', '-date_of_translation', 'glyphicon glyphicon-arrow-up'),
        ('rate', '-visual_novel__rate', 'glyphicon glyphicon-arrow-up'),
        ('rate', 'visual_novel__rate', 'glyphicon glyphicon-arrow-down'),
        ('date_of_release', 'visual_novel__date_of_release', 'glyphicon glyphicon-arrow-down'),
        ('date_of_release', '-visual_novel__date_of_release', 'glyphicon glyphicon-arrow-up'),
        ('title', 'visual_novel__title', 'glyphicon glyphicon-arrow-down'),
        ('title', '-visual_novel__title', 'glyphicon glyphicon-arrow-up'),
        ('popularity', '-visual_novel__popularity', 'glyphicon glyphicon-arrow-up'),
        ('popularity', 'visual_novel__popularity', 'glyphicon glyphicon-arrow-down'),
    ]
    # This is base data for providing icons and links, in case nothing is selected by user
    context['date_of_translation'] = '-date_of_translation'
    context['date_of_translation_icon'] = 'glyphicon glyphicon-arrow-down'
    context['rate'] = '-visual_novel__rate'
    context['rate_icon'] = ''
    context['date_of_release'] = '-visual_novel__date_of_release'
    context['date_of_release_icon'] = ''
    context['title'] = 'visual_novel__title'
    context['title_icon'] = ''
    context['popularity'] = '-visual_novel__popularity'
    context['popularity_icon'] = ''
    context['base_poster_url'] = config.CHART_POSTER_NOT_LOADED_IMAGE or settings.POSTER_STOPPER_URL
    # In case of sort selected, sort and provide respective links and icons
    if sort_by and sort_by in all_sortings:
        all_chart_items = all_chart_items.order_by(sort_by)
        idx = all_sortings.index(sort_by)
        context['date_of_translation_icon'] = '' # Removing icon for default sort in order to prevent multiple icons
        context[all_sortings_context_links[idx][0]] = all_sortings_context_links[idx][1]
        context[all_sortings_context_links[idx][0] + '_icon'] = all_sortings_context_links[idx][2]
        cache_key += '_sort_{}'.format(sort_by)
    else:
        cache_key += '_sort_{}'.format(base_sort_by)
        all_chart_items = all_chart_items.order_by(base_sort_by)

    all_chart_items_data = ChartItemListSerializer(all_chart_items, many=True).data

    # Visual novels are grouped in list in groups of settings.CHART_NUMBER_OF_VN_IN_ROW
    k = 0
    row = list()
    for chart_item in all_chart_items_data:
        row.append(chart_item)
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
            'link': reverse('chart_index_with_genre', kwargs={'genre_alias': genre.genre.alias}),
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
            'link': reverse('chart_index_with_studio', kwargs={'studio_alias': studio.studio.alias}),
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
            'link': reverse('chart_index_with_tag', kwargs={'tag_alias': tag.tag.alias}),
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
            'link': reverse('chart_index_with_staff', kwargs={'staff_alias': staff.alias}),
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
            'link': reverse('chart_index_with_translator', kwargs={'translator_alias': translator.translator.alias}),
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
