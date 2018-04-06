from django.shortcuts import render
from django.conf import settings


def handler404(request, exception, template_name='404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response

