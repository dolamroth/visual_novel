from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied


class IsAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, **kwargs):
        user = request.user
        if not bool(user.is_authenticated) or not hasattr(user, 'profile') or not bool(user.profile.email_confirmed):
            return HttpResponseRedirect("/login?next=" + request.path)

        response = self.get_response(request, **kwargs)
        return response


class HasPermissionToEditProfile:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, **kwargs):
        username = kwargs.get('username', None)
        if not (username == request.user.username):
            raise PermissionDenied

        response = self.get_response(request, **kwargs)
        return response
