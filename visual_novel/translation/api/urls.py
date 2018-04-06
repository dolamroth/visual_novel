from django.urls import path

from . import views as translation_api_views

urlpatterns = [
    path(r'<str:vn_alias>/edit', translation_api_views.edit_chapter, name='chapter_edit'),
    path(r'<str:vn_alias>/add', translation_api_views.add_chapter, name='chapter_add'),
    path(r'<str:vn_alias>/get-children', translation_api_views.get_chapter_children, name='chapter_get_children'),
    path(r'<str:vn_alias>/delete-chapter', translation_api_views.delete_translation_chapter, name='chapter_delete'),
    path(r'<str:vn_alias>/get-statistics',
         translation_api_views.get_current_statistics_for_translation_item, name='get_statistics'),
    path(r'<str:vn_alias>/edit-comment',
         translation_api_views.get_edit_pictures_tech_comment_statistics, name='edit_comment'),
]