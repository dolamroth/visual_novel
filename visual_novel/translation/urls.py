from django.urls import path, include

from . import views as translation_views
from .api import urls as api_urls

urlpatterns = [
    path(r'<str:vn_alias>/edit', translation_views.edit_statistics, name='statistics_edit'),
]
