from django.urls import path

from . import views as translation_api_views

urlpatterns = [
    path(r'all', translation_api_views.translation_list, name='get_translation_list'),
    path(r'all/selects', translation_api_views.translation_list_data_selects, name='get_translation_list_selects'),
    path(r'<str:vn_alias>/edit', translation_api_views.edit_chapter, name='chapter_edit'),
    path(r'<str:vn_alias>/add', translation_api_views.add_chapter, name='chapter_add'),
    path(r'<str:vn_alias>/get-children', translation_api_views.get_chapter_children, name='chapter_get_children'),
    path(r'<str:vn_alias>/delete-chapter', translation_api_views.delete_translation_chapter, name='chapter_delete'),
    path(r'<str:vn_alias>/get-statistics',
         translation_api_views.get_current_statistics_for_translation_item, name='get_statistics'),
    path(r'<str:vn_alias>/edit-comment',
         translation_api_views.get_edit_pictures_tech_comment_statistics, name='edit_comment'),
    path(r'<str:vn_alias>/addbetalink',
         translation_api_views.manage_betalink, name='add_beta_link'),
    path(r'<str:vn_alias>/editbetalink',
         translation_api_views.manage_betalink, name='edit_beta_link'),
    path(r'<str:vn_alias>/deletebetalink',
         translation_api_views.delete_betalink, name='delete_beta_link'),
    path(r'<str:vn_alias>/change-status',
         translation_api_views.change_status, name='change_translation_status'),
]
