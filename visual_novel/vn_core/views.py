from django.core.management import call_command
from django.http.response import HttpResponseRedirect

from core.middlewares import IsSuperuserMiddleware


@IsSuperuserMiddleware
def clear_cache_view(request):
    call_command("clear_cache")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
