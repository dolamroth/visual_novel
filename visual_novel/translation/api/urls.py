from django.urls import path

from . import views as translation_api_views

urlpatterns = [
    path(r'<str:vn_alias>/edit', translation_api_views.edit_chapter, name='chapter_edit'),
]
