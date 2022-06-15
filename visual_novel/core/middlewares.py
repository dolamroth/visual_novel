from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin


class IsAuthenticatedMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if not bool(user.is_authenticated) \
                or not hasattr(user, 'profile') \
                or not bool(user.profile.email_confirmed):
            return HttpResponseRedirect("/login?next=" + request.path)
        else:
            return None


class HasPermissionToEditProfile(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        username = view_kwargs.get('username', None)
        if not (username == request.user.username):
            raise PermissionDenied
        return None
