from django.urls import path

from . import views as translation_views

urlpatterns = [
    path(r'<str:vn_alias>/edit', translation_views.edit_statistics, name='statistics_edit'),
]
