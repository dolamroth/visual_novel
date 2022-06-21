import mimetypes

from .base import *

DEBUG = True

mimetypes.add_type("application/javascript", ".js", True)

STATICFILES_DIRS = [
	Path(BASE_DIR, "static"),
]

ALLOWED_HOSTS += ['127.0.0.1']

INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',

	'debug_toolbar.middleware.DebugToolbarMiddleware',

	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'corsheaders.middleware.CorsMiddleware',
]

INTERNAL_IPS = [
	"127.0.0.1",
]

DEBUG_TOOLBAR_PANELS = [
	'debug_toolbar.panels.timer.TimerPanel',
	'debug_toolbar.panels.settings.SettingsPanel',
	'debug_toolbar.panels.headers.HeadersPanel',
	'debug_toolbar.panels.request.RequestPanel',
	'debug_toolbar.panels.sql.SQLPanel',
	'debug_toolbar.panels.staticfiles.StaticFilesPanel',
	'debug_toolbar.panels.templates.TemplatesPanel',
	'debug_toolbar.panels.cache.CachePanel',
	'debug_toolbar.panels.signals.SignalsPanel',
	'debug_toolbar.panels.logging.LoggingPanel',
	'debug_toolbar.panels.redirects.RedirectsPanel',
]

CACHES = {
	"default": {
		"BACKEND": "django.core.cache.backends.db.DatabaseCache",
		"LOCATION": "cache_table_for_local_development"
	}
}

WSGI_APPLICATION = None
