import json

from constance import config

from django.conf import settings
from django.core.cache import caches
from django.db.models import Q

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as restValidationError
from rest_framework.renderers import JSONRenderer

from core.middlewares import IsAuthenticatedMiddleware
from ..middlewares import HasPermissionToEditVNMiddleware
from ..utils import select_like_statistics_name, get_status_tuple_for_translation_item

from ..choices import TRANSLATION_ITEMS_STATUSES
from ..commands import (
    EditTranslationChapter, EditTranslationPartChapter, AddTranslationPartChapter, AddTranslationChapter,
    DeleteTranslationChapter, ManageBetaLink, DeleteBetaLink, ChangeTranslationStatus
)
from ..errors import (
    InvalidMoveToChildElement, TranslationNotFound, InvalidValueOnRowsQuantity, InvalidMoveParent,
    CannotBeSiblingOfBaseTreeNode, ParentDoesNotExist, InvalidBetaLinkUrl, BetaLinkUrlAlreadyExists,
    BetaLinkDoesNotExist, TranslationStatusDoesNotExist, TranslationCannotBeEditedDueToStatus
)
from .serializers import (
    TranslationChapterSerializer, TranslationChapterPartSerializer, AddTranslationChapterSerializer, StatisticsComment,
    AddTranslationChapterPartSerializer, StatisticsDescription, BetaLinkSerializer, TranslationListShortSerializer
)
from ..models import (
    TranslationStatisticsChapter, TranslationItem, TranslationStatistics, TranslationSubscription
)

cache = caches['default']


def get_data(request):
    data = dict()
    data['translation_item_id'] = request.GET.get('translation_item_id', None)
    data['translation_chapter_id'] = request.GET.get('translation_chapter_id', None)
    data['new_parent'] = request.GET.get('parent', None)
    data['new_move_to'] = request.GET.get('move_to', None)
    data['script_title'] = request.GET.get('script_title', None)
    data['total'] = request.GET.get('total', None)
    data['new_translated'] = request.GET.get('translated', None)
    data['new_edited_first_pass'] = request.GET.get('edited_first_pass', None)
    data['new_edited_second_pass'] = request.GET.get('edited_second_pass', None)

    data['title'] = request.GET.get('title', None)
    if not data['title']:
        data['title'] = data['script_title']

    is_chapter = (request.GET.get('is_chapter', None) == 'true')

    return data, is_chapter


@IsAuthenticatedMiddleware
@HasPermissionToEditVNMiddleware
@api_view(['GET', 'POST', ])
def edit_chapter(request, vn_alias):

    data, is_chapter = get_data(request)

    if is_chapter:
        serializer = TranslationChapterPartSerializer(data=data, context={'user': request.user})
    else:
        serializer = TranslationChapterSerializer(data=data, context={'user': request.user})

    try:
        serializer.is_valid(raise_exception=True)
    except restValidationError as exc:
        return Response(data={
            'message': 'При попытке сохранения возникли ошибки.',
            'errors': serializer.errors
        }, status=422)

    try:
        if settings.PRODUCTION_FLAG:
            with cache.lock('translation_item_{}'.format(data['translation_item_id'])):
                if is_chapter:
                    translation_chapter, movement = EditTranslationPartChapter(serializer.data).execute()
                else:
                    translation_chapter, movement = EditTranslationChapter(serializer.data).execute()
        else:
            if is_chapter:
                translation_chapter, movement = EditTranslationPartChapter(serializer.data).execute()
            else:
                translation_chapter, movement = EditTranslationChapter(serializer.data).execute()
    except TranslationNotFound as exc:
        return Response(data={'message': exc.message}, status=404)
    except (
            InvalidMoveToChildElement, InvalidValueOnRowsQuantity, InvalidMoveParent, CannotBeSiblingOfBaseTreeNode,
            ParentDoesNotExist, TranslationCannotBeEditedDueToStatus
    ) as exc:
        return Response(data={'message': exc.message}, status=422)

    return_data = {**serializer.data}
    return_data.pop('timezone')

    return Response(data={
        'message': 'Операция проведена успешно.',
        'movement': movement,
        'data': return_data
    }, status=200)


@IsAuthenticatedMiddleware
@HasPermissionToEditVNMiddleware
@api_view(['GET', 'POST', ])
def add_chapter(request, vn_alias):

    data, is_chapter = get_data(request)
    data['is_chapter'] = is_chapter

    if is_chapter:
        serializer = AddTranslationChapterPartSerializer(data=data, context={'user': request.user})
    else:
        serializer = AddTranslationChapterSerializer(data=data, context={'user': request.user})

    try:
        serializer.is_valid(raise_exception=True)
    except restValidationError as exc:
        return Response(data={
            'message': 'При попытке добавления возникли ошибки.',
            'errors': serializer.errors
        }, status=422)

    try:
        if settings.PRODUCTION_FLAG:
            with cache.lock('translation_item_{}'.format(data['translation_item_id'])):
                if is_chapter:
                    translation_chapter = AddTranslationPartChapter(serializer.data).execute()
                else:
                    translation_chapter = AddTranslationChapter(serializer.data).execute()
        else:
            if is_chapter:
                translation_chapter = AddTranslationPartChapter(serializer.data).execute()
            else:
                translation_chapter = AddTranslationChapter(serializer.data).execute()
    except TranslationNotFound as exc:
        return Response(data={'message': exc.message}, status=404)
    except (
        InvalidMoveToChildElement, InvalidValueOnRowsQuantity, InvalidMoveParent, CannotBeSiblingOfBaseTreeNode,
        ParentDoesNotExist, TranslationCannotBeEditedDueToStatus
    ) as exc:
        return Response(data={'message': exc.message}, status=422)

    return Response(data={
        'message': 'Операция проведена успешно.',
        'id': translation_chapter.id
    }, status=200)


@IsAuthenticatedMiddleware
@HasPermissionToEditVNMiddleware
@api_view(['GET', 'POST', ])
def get_chapter_children(request, vn_alias):
    translation_chapter_id = request.GET.get('translation_chapter_id', None)
    try:
        translation_chapter_id = int(translation_chapter_id)
    except (ValueError, TypeError):
        return Response(data={'message': "Неверный формат идентификатора главы."}, status=422)

    try:
        translation_chapter = TranslationStatisticsChapter.objects.get(id=translation_chapter_id)
    except TranslationStatisticsChapter.DoesNotExist:
        return Response(data={'message': TranslationNotFound().message}, status=422)

    children = [{
        'title': select_like_statistics_name(d, base_level=translation_chapter.level)
    } for d in translation_chapter.get_descendants(include_self=True)]

    return Response(data={
        'message': 'Операция проведена успешно.',
        'children': children
    }, status=200)


@IsAuthenticatedMiddleware
@HasPermissionToEditVNMiddleware
@api_view(['GET', 'POST', ])
def delete_translation_chapter(request, vn_alias):

    data, is_chapter = get_data(request)

    try:
        if settings.PRODUCTION_FLAG:
            with cache.lock('translation_item_{}'.format(data['translation_item_id'])):
                deleted_n = DeleteTranslationChapter(data).execute()
        else:
            deleted_n = DeleteTranslationChapter(data).execute()
    except TranslationNotFound as exc:
        return Response(data={'message': exc.message}, status=404)
    except TranslationCannotBeEditedDueToStatus as exc:
        return Response(data={'message': exc.message}, status=422)

    return Response(data={
        'message': 'Операция проведена успешно.',
        'delete_results': deleted_n
    }, status=200)


@IsAuthenticatedMiddleware
@HasPermissionToEditVNMiddleware
@api_view(['GET', 'POST', ])
def get_current_statistics_for_translation_item(request, vn_alias):

    data, is_chapter = get_data(request)

    try:
        tree_id = TranslationItem.objects.get(
            id=int(data['translation_item_id']),
            visual_novel__is_published=True,
            is_published=True
        ).statistics.tree_id
        base_node = TranslationStatisticsChapter.objects.get(lft=1, tree_id=tree_id)
        data = {
            'total_rows': base_node.total_rows,
            'translated': base_node.translated,
            'edited_first_pass': base_node.edited_first_pass,
            'edited_second_pass': base_node.edited_second_pass
        }
    except (TranslationItem.DoesNotExist, ValueError, TranslationStatisticsChapter.DoesNotExist):
        return Response(data={'message': TranslationNotFound().message}, status=404)

    return Response(data={
        'message': 'Операция проведена успешно.',
        'statistics': data
    }, status=200)


@IsAuthenticatedMiddleware
@HasPermissionToEditVNMiddleware
@api_view(['GET', 'POST', ])
def get_edit_pictures_tech_comment_statistics(request, vn_alias):

    description = request.GET.get('description', None)
    translation_item_id = request.GET.get('translation_item_id', None)
    type = request.GET.get('type', None)

    if not type in ['pictures', 'tech', 'comment']:
        return Response(data={
            'message': 'Неизвестный тип запроса.'
        }, status=422)

    if type == 'comment':
        serializer = StatisticsComment(data={'comment': description})
    else:
        serializer = StatisticsDescription(data={'description': description})

    try:
        translation_item_id = int(translation_item_id)
        translation_item = TranslationItem.objects.get(
            id=translation_item_id,
            visual_novel__is_published=True,
            is_published=True
        )
        translation_statistics = TranslationStatistics.objects.get(pk=translation_item.statistics.pk)
    except (TypeError, TranslationItem.DoesNotExist, TranslationStatistics.DoesNotExist):
        return Response(data={
            'message': 'Перевод с указанным идентификатором не найден.'
        }, status=404)

    status_tuple = get_status_tuple_for_translation_item(translation_item)
    if not status_tuple[6]:
        return Response(data={
            'message': TranslationCannotBeEditedDueToStatus().message
        }, status=422)

    try:
        serializer.is_valid(raise_exception=True)
    except restValidationError as exc:
        return Response(data={
            'message': 'При попытке сохранения возникли ошибки.',
            'errors': serializer.errors
        }, status=422)

    if type == 'pictures':
        translation_statistics.pictures_statistics = description
    elif type == 'tech':
        translation_statistics.technical_statistics = description
    else:
        translation_statistics.comment = description
    translation_statistics.save()

    return Response(data={
        'message': 'Операция проведена успешно.',
        'description': description,
        'type': type
    }, status=200)


@IsAuthenticatedMiddleware
@HasPermissionToEditVNMiddleware
@api_view(['GET', 'POST', ])
def manage_betalink(request, vn_alias):

    data = {
        'translation_item_id': request.GET.get('data_translation_item', None),
        'title': request.GET.get('title', None),
        'url': request.GET.get('url', None),
        'comment': request.GET.get('comment', ''),
        'betalink_id': request.GET.get('betalink_id', 0),
    }

    serializer = BetaLinkSerializer(data=data, context={'user': request.user})

    try:
        serializer.is_valid(raise_exception=True)
    except restValidationError as exc:
        return Response(data={
            'message': 'При попытке сохранения возникли ошибки.',
            'errors': serializer.errors
        }, status=422)

    try:
        betalink_id, approved, rejected = ManageBetaLink(serializer.data).execute()
    except (TranslationNotFound, InvalidBetaLinkUrl, BetaLinkUrlAlreadyExists, BetaLinkDoesNotExist) as exc:
        return Response(data={'message': exc.message}, status=422)

    return_data = {**serializer.data}
    return_data.pop('timezone', None)
    return_data['approved'] = "True" if approved else "False"
    return_data['rejected'] = "True" if rejected else "False"
    return_data['betalink_id'] = betalink_id

    return Response(data={
        'message': 'Операция проведена успешно.',
        'data': return_data
    }, status=200)


@IsAuthenticatedMiddleware
@HasPermissionToEditVNMiddleware
@api_view(['GET', 'POST', ])
def delete_betalink(request, vn_alias):

    data = {
        'betalink_id': request.GET.get('betalink_id', 0),
    }

    try:
        deleted_n = DeleteBetaLink(data).execute()
    except BetaLinkDoesNotExist as exc:
        return Response(data={'message': exc.message}, status=404)

    return Response(data={
        'message': 'Операция проведена успешно.',
        'delete_results': deleted_n
    }, status=200)


@IsAuthenticatedMiddleware
@HasPermissionToEditVNMiddleware
@api_view(['GET', 'POST', ])
def change_status(request, vn_alias):

    status_key = request.GET.get('status', None)
    translation_item_id = request.GET.get('translation_item_id', 0)

    try:
        ChangeTranslationStatus(status_key, translation_item_id).execute()
    except (TranslationNotFound, TranslationStatusDoesNotExist) as exc:
        return Response(data={'message': exc.message}, status=404)

    return Response(data={
        'message': 'Операция проведена успешно.'
    }, status=200)


@api_view(['GET', 'POST', ])
@renderer_classes((JSONRenderer,))
def translation_list(request):

    try:
        selected_statuses = json.loads(request.GET.get('statuses', '[]'))
        selected_translators = json.loads(request.GET.get('translators', '[]'))
    except json.decoder.JSONDecodeError:
        return Response({})

    all_status_keys = list(TranslationItem.status)
    all_status_int_keys = list()
    k = 1
    for status in all_status_keys:
        selected_status = [d for d in selected_statuses if d['key']==status]
        if len(selected_status) == 0:
            continue
        selected_status = selected_status[0]
        if selected_status['checked']:
            all_status_int_keys.append(k)
        k *= 2

    selected_translators_ids = [d['id'] for d in selected_translators if d['checked']]

    all_translations = TranslationItem.objects.filter(
        is_published=True,
        visual_novel__is_published=True,
        status__in=all_status_int_keys
    )

    if 0 in selected_translators_ids:
        all_translations = all_translations\
            .filter(Q(translator__in=selected_translators_ids)| Q(translator__isnull=True))
    else:
        all_translations = all_translations.filter(translator__in=selected_translators_ids)

    all_translations = all_translations.order_by('visual_novel__title')

    serializer = TranslationListShortSerializer(all_translations, context={'user': request.user}, many=True)

    return Response({'translations': serializer.data})


@api_view(['GET', 'POST', ])
@renderer_classes((JSONRenderer,))
def translation_list_data_selects(request):
    context = dict()

    # List of all statuses
    context['statuses'] = list()
    default_statuses = config.DEFAULT_TRANSLATION_STATUSES_TO_SHOW.split(',')
    for translation_status in TRANSLATION_ITEMS_STATUSES:
        context['statuses'].append({
            'key': translation_status.alias,
            'name': translation_status.name,
            'style': translation_status.style,
            'default': translation_status.alias in default_statuses
        })

    # List of all translators
    context['translators'] = list()
    all_translators = list(
        TranslationItem.objects.filter(is_published=True)
            .values_list('translator', 'translator__title').distinct().order_by('translator__title')
    )
    for translator in all_translators:
        context['translators'].append({
            'id': translator[0] or 0,
            'name': translator[1] or 'Не указано'
        })

    return Response(context)
