from django.http import HttpResponseRedirect


class HasPermissionToEditVNMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        vn_alias = view_kwargs.get('vn_alias', None)
        # TODO: change condition and redirect link
        if not request.user.is_superuser:
            return HttpResponseRedirect("/login?next=" + request.path)
        else:
            return None