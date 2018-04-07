from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied


class IsAuthenticatedMiddleware(object):
    def process_request(self, request):
        if not bool(request.user.is_authenticated):
            return HttpResponseRedirect("/login?next=" + request.path)
        else:
            return None


class HasPermissionToEditProfile(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        username = view_kwargs.get('username', None)
        if not (username == request.user.username):
            raise PermissionDenied
        return None
