from django.utils.decorators import decorator_from_middleware

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as restValidationError

from core.middlewares import IsAuthenticatedMiddleware
from translation.middlewares import HasPermissionToEditVNMiddleware

from ..commands import EditTranslationChapter, EditTranslationPartChapter
from ..errors import (
    InvalidMoveToChildElement, TranslationNotFound, InvalidValueOnRowsQuantity, InvalidMoveParent
)
from .serializers import TranslationChapterSerializer, TranslationChapterPartSerializer


@api_view(['GET', 'POST', ])
@decorator_from_middleware(IsAuthenticatedMiddleware)
@decorator_from_middleware(HasPermissionToEditVNMiddleware)
def edit_chapter(request, vn_alias):

    data = {
        'translation_item_id': request.GET.get('translation_item_id', None),
        'translation_chapter_id': request.GET.get('translation_chapter_id', None),
        'new_parent': request.GET.get('parent', None),
        'new_move_to': request.GET.get('move_to', None),
        'title': request.GET.get('title', None),
        'script_title': request.GET.get('script_title', None),
        'total': request.GET.get('total', None),
        'new_translated': request.GET.get('translated', None),
        'new_edited_first_pass': request.GET.get('edited_first_pass', None),
        'new_edited_second_pass': request.GET.get('edited_second_pass', None)
    }

    is_chapter = (request.GET.get('is_chapter', None) == 'true')

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
    except (InvalidMoveToChildElement, InvalidValueOnRowsQuantity, InvalidMoveParent) as exc:
        return Response(data={'message': exc.message}, status=422)

    return_data = {**serializer.data}
    return_data.pop('timezone')

    return Response(data={
        'message': 'Операция проведена успешно.',
        'movement': movement,
        'data': return_data
    }, status=200)
