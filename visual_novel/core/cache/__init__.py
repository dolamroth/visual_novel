# ALL CREDITS GO TO https://bitbucket.org/kmike/django-view-cache-utils/src/4408ad8f1751ee2fccb441d2a342c4ed710467a0/...
# ... view_cache_utils/__init__.py?at=default&fileviewer=file-view-default

from constance import config

from django.conf import settings
from django.utils.decorators import decorator_from_middleware_with_args
from .middleware import CacheMiddleware


def custom_key_prefix(request, base_prefix='', headers=[], get_params=[]):
    result = 'query-cache'

    if base_prefix:
        result = result + '-' + str(base_prefix).replace('_', '-')

    result = result + 'path{}'.format(request.path.replace('/', '-'))

    for header in headers:
        header_name = header.upper()
        header_value = request.META.get(header_name, request.META.get('HTTP_' + header_name, None))
        header_key = header.lower().replace('_', '-')
        if header_value:
            result = result + '-{}-{}'.format(header_key, str(header_value).replace('_', '-'))

    for get_param in get_params:
        get_value = request.GET.get(get_param, None)
        get_key = get_param.lower().replace('_', '-')
        if get_value:
            result = result + '-{}-{}'.format(get_key, str(get_value).replace('_', '-'))

    return result


def custom_cache(*args, **kwargs):
    time_of_cache_living = config.REDIS_CACHE_TIME_LIFE
    if len(args) > 0 and type(args[0]) == int and args[0] > 0:
        time_of_cache_living = args[0]

    # Инициализация переменных
    base_prefix = ''
    headers = []
    get_params = []

    if 'base_prefix' in kwargs.keys():
        base_prefix = kwargs['base_prefix']

    if 'headers' in kwargs.keys():
        headers = kwargs['headers']

    if 'get_params' in kwargs.keys():
        get_params = kwargs['get_params']

    return decorator_from_middleware_with_args(CacheMiddleware)(
        cache_timeout=time_of_cache_living,
        key_prefix=custom_key_prefix,
        base_prefix=base_prefix,
        headers=headers,
        get_params=get_params
    )
