from .base import *

DEBUG = True

STATIC_ROOT = os.path.join(BASE_DIR, '')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

ALLOWED_HOSTS += ['127.0.0.1']
