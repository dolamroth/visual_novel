from .base import *

DEBUG = False

ALLOWED_HOSTS += ['185.228.233.21', 'www.vn-russian.ru']

PRODUCTION_FLAG = True

REDIS_HOST = get_secret(section='REDIS', setting='HOST')
REDIS_PORT = get_secret(section='REDIS', setting='PORT')
REDIS_DB = get_secret(section='REDIS', setting='DB')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
