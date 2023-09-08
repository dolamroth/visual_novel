from django.http import Http404
from django.core.exceptions import PermissionDenied

from translation.models import TranslationItem


class HasPermissionToEditVNMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, **kwargs):
        vn_alias = kwargs.get('vn_alias', None)
        try:
            translation = TranslationItem.objects.get(visual_novel__alias=vn_alias)
        except TranslationItem.DoesNotExist:
            raise Http404
        user_moderates_vn = (request.user in translation.moderators.all())
        if not (request.user.is_superuser or request.user.is_staff or user_moderates_vn):
            raise PermissionDenied

        response = self.get_response(request, **kwargs)
        return response
