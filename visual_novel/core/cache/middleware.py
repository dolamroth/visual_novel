# ALL CREDITS GO TO https://bitbucket.org/kmike/django-view-cache-utils/src/4408ad8f1751ee2fccb441d2a342c4ed710467a0/...
# ... view_cache_utils/middleware.py?at=default&fileviewer=file-view-default

from constance import config

from django.conf import settings
from django.core.cache import caches
from django.utils.cache import patch_response_headers, get_max_age

# Выбираем кастомный кеш, чтобы получить кеш типа RedisCache (на боевом сервере)
cache = caches['default']


class UpdateCacheMiddleware(object):
    def __init__(self):
        # Нужно только для инициализации. Перезаписывается в __init__() CacheMiddleware
        self.cache_timeout = config.REDIS_CACHE_TIME_LIFE
        self.key_prefix = 'custom-cache'
        self.base_prefix = ''
        self.headers = []
        self.get_params = []

    def process_response(self, request, response):
        # Параметр _cache_update_cache прописывается в process_request
        if not hasattr(request, '_cache_update_cache') or not request._cache_update_cache:
            return response

        if request.method != 'GET':
            return response
        if not response.status_code == 200:
            return response

        timeout = get_max_age(response)
        if timeout == None:
            timeout = self.cache_timeout
        elif timeout == 0:
            return response
        patch_response_headers(response, timeout)

        if timeout:
            if callable(self.key_prefix):
                key_prefix = self.key_prefix(request,
                                base_prefix=self.base_prefix, headers=self.headers, get_params=self.get_params)
            else:
                key_prefix = self.key_prefix

            cache_key = key_prefix
            cache.set(cache_key, response, timeout)
        return response


class FetchFromCacheMiddleware(object):
    def __init__(self):
        # Нужно только для инициализации. Перезаписывается в __init__() CacheMiddleware
        self.cache_timeout = config.REDIS_CACHE_TIME_LIFE
        self.key_prefix = 'custom-cache'
        self.base_prefix = ''
        self.headers = []
        self.get_params = []

    def process_request(self, request):

        if not request.method in ('GET', 'HEAD'):
            request._cache_update_cache = False
            return None

        if request.GET and not callable(self.key_prefix):
            request._cache_update_cache = False
            return None

        if callable(self.key_prefix):
            key_prefix = self.key_prefix(request,
                                base_prefix=self.base_prefix, headers=self.headers, get_params=self.get_params)
            if key_prefix is None:
                request._cache_update_cache = False
                return None
        else:
            key_prefix = self.key_prefix

        cache_key = key_prefix
        if cache_key is None:
            request._cache_update_cache = True
            return None

        response = cache.get(cache_key, None)
        if response is None:
            request._cache_update_cache = True
            return None

        request._cache_update_cache = False
        return response


class CacheMiddleware(UpdateCacheMiddleware, FetchFromCacheMiddleware):
    def __init__(self, cache_timeout=None, key_prefix=None, base_prefix='', headers=[], get_params=[]):
        self.cache_timeout = cache_timeout
        self.key_prefix = key_prefix
        self.base_prefix = base_prefix
        self.headers = headers
        self.get_params = get_params