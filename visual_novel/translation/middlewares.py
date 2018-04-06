from rest_framework.exceptions import PermissionDenied


class HasPermissionToEditVNMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        vn_alias = view_kwargs.get('vn_alias', None)
        # TODO: change condition
        if not request.user.is_superuser:
            raise PermissionDenied(detail="Недостаточно прав для просмотра или изменения данного объекта.")
        else:
            return None
