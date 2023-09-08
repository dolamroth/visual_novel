import django.utils.encoding
django.utils.encoding.smart_text = django.utils.encoding.smart_str

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visual_novel.settings')

application = get_wsgi_application()
