from django.utils.decorators import decorator_from_middleware

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as restValidationError

from core.middlewares import IsAuthenticatedMiddleware
from translation.middlewares import HasPermissionToEditVNMiddleware

from ..commands import (
    EditTranslationChapter, EditTranslationPartChapter, AddTranslationPartChapter, AddTranslationChapter
)
from ..errors import (
    InvalidMoveToChildElement, TranslationNotFound, InvalidValueOnRowsQuantity, InvalidMoveParent,
    CannotBeSiblingOfBaseTreeNode, ParentDoesNotExist
)
from .serializers import (
    TranslationChapterSerializer, TranslationChapterPartSerializer,
    AddTranslationChapterPartSerializer, AddTranslationChapterSerializer
)


def get_data(request):
    data = {
        'translation_item_id': request.GET.get('translation_item_id', None),
        'translation_chapter_id': request.GET.get('translation_chapter_id', None),
        'new_parent': request.GET.get('parent', None),
        'new_move_to': request.GET.get('move_to', None),
        'script_title': request.GET.get('script_title', None),
        'total': request.GET.get('total', None),
        'new_translated': request.GET.get('translated', None),
        'new_edited_first_pass': request.GET.get('edited_first_pass', None),
        'new_edited_second_pass': request.GET.get('edited_second_pass', None)
    }

    data['title'] = request.GET.get('script_title', data['script_title'])
    is_chapter = (request.GET.get('is_chapter', None) == 'true')

    return data, is_chapter


@api_view(['GET', 'POST', ])
@decorator_from_middleware(IsAuthenticatedMiddleware)
@decorator_from_middleware(HasPermissionToEditVNMiddleware)
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
        if is_chapter:
            translation_chapter, movement = EditTranslationPartChapter(serializer.data).execute()
        else:
            translation_chapter, movement = EditTranslationChapter(serializer.data).execute()
    except TranslationNotFound as exc:
        return Response(data={'message': exc.message}, status=404)
    except (
            InvalidMoveToChildElement, InvalidValueOnRowsQuantity, InvalidMoveParent, CannotBeSiblingOfBaseTreeNode,
            ParentDoesNotExist
    ) as exc:
        return Response(data={'message': exc.message}, status=422)

    return_data = {**serializer.data}
    return_data.pop('timezone')

    return Response(data={
        'message': 'Операция проведена успешно.',
        'movement': movement,
        'data': return_data
    }, status=200)


@api_view(['GET', 'POST', ])
@decorator_from_middleware(IsAuthenticatedMiddleware)
@decorator_from_middleware(HasPermissionToEditVNMiddleware)
def add_chapter(request, vn_alias):

    data, is_chapter = get_data(request)

    print(data, is_chapter)

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
        if is_chapter:
            translation_chapter = AddTranslationPartChapter(serializer.data).execute()
        else:
            translation_chapter = AddTranslationChapter(serializer.data).execute()
    except TranslationNotFound as exc:
        return Response(data={'message': exc.message}, status=404)
    except (
        InvalidMoveToChildElement, InvalidValueOnRowsQuantity, InvalidMoveParent, CannotBeSiblingOfBaseTreeNode,
        ParentDoesNotExist
    ) as exc:
        return Response(data={'message': exc.message}, status=422)

    return Response(data={
        'message': 'Операция проведена успешно.',
        'id': translation_chapter.id
    }, status=200)
