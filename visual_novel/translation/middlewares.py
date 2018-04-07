from django.http import Http404
from django.core.exceptions import PermissionDenied

from translation.models import TranslationItem


class HasPermissionToEditVNMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        vn_alias = view_kwargs.get('vn_alias', None)
        try:
            translation = TranslationItem.objects.get(visual_novel__alias=vn_alias)
        except TranslationItem.DoesNotExist:
            raise Http404
        user_moderates_vn = (request.user in translation.moderators.all())
        if not (request.user.is_superuser or request.user.is_staff or user_moderates_vn):
            raise PermissionDenied
        else:
            return None
