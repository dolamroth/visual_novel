from django.shortcuts import render
from django.http.response import JsonResponse

from core.yandex_api import addr_query_yandex


def handler404(request, exception, template_name='404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response


def yandex_view(request):
    if request.GET.get('query', None):
        return JsonResponse(addr_query_yandex(request.GET.get('query')), safe=True)
    else:
        return JsonResponse({})
