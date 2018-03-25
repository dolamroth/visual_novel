from django.http import HttpResponseRedirect


class IsAuthenticatedMiddleware(object):
    def process_request(self, request):
        if not bool(request.user.is_authenticated):
            return HttpResponseRedirect("/login?next=" + request.path)
        else:
            return None
