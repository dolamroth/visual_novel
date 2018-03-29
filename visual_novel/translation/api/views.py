from django.http import Http404
from django.utils.decorators import decorator_from_middleware
from django.conf import settings

from core.exceptions import Conflict

from core.middlewares import IsAuthenticatedMiddleware
from translation.middlewares import HasPermissionToEditVNMiddleware

from ..commands import EditTranslationChapter
from ..errors import (
    InvalidMoveToChildElement, TranslationNotFound, InvalidRowsQuantityInput, InvalidValueOnRowsQuantity
)


@decorator_from_middleware(IsAuthenticatedMiddleware)
@decorator_from_middleware(HasPermissionToEditVNMiddleware)
def edit_chapter(request, vn_alias):
    translation_item_id = request.GET.get('translation_item_id', None)
    translation_chapter_id = request.GET.get('translation_chapter_id', None)
    new_total = request.GET.get('total', None)
    new_translated = request.GET.get('translated', None)
    new_edited_first_pass = request.GET.get('edited_first_pass', None)
    new_edited_second_pass = request.GET.get('edited_second_pass', None)
    new_parent = request.GET.get('parent', None)
    new_move_to = request.GET.get('move_to', None)
    is_chapter = request.GET.get('is_chapter', None)
    user=request.user
    if hasattr(user, 'profile') and user.profile.timezone:
        timezone = user.profile.timezone
    else:
        timezone = settings.DEFAULT_TIME_ZONE

    try:
        translation_chapter = EditTranslationChapter(
            translation_item_id,
            translation_chapter_id,
            new_total,
            new_translated,
            new_edited_first_pass,
            new_edited_second_pass,
            new_parent,
            new_move_to,
            is_chapter,
            timezone
        ).execute()
    except TranslationNotFound as exc:
        raise Conflict(detail=exc.message)
    except InvalidMoveToChildElement as exc:
        raise Conflict(detail=exc.message)
    except InvalidRowsQuantityInput as exc:
        raise Conflict(detail=exc.message)
    except InvalidValueOnRowsQuantity as exc:
        raise Conflict(detail=exc.message)

    pass
