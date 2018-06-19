from django.urls import path

from . import views as translation_views

urlpatterns = [
    path(r'<str:vn_alias>/edit', translation_views.edit_statistics, name='statistics_edit'),
    path(r'all', translation_views.all_translations, name='translations_all'),
    path(r'<str:vn_alias>', translation_views.translation_item_view, name='translation_item'),
]
