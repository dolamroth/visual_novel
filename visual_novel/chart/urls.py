from django.urls import path

from . import views as chart_views

app_name = 'chart'
urlpatterns = [
    path('<str:vn_alias>', chart_views.chart_page, name='detail_chart'),
    path('', chart_views.chart_index_page, name='chart_index'),
    path('genre/<str:genre_alias>', chart_views.chart_index_page, name='chart_index_with_genre'),
    path('tag/<str:tag_alias>', chart_views.chart_index_page, name='chart_index_with_tag'),
    path('studio/<str:studio_alias>', chart_views.chart_index_page, name='chart_index_with_studio'),
    path('staff/<str:staff_alias>', chart_views.chart_index_page, name='chart_index_with_staff'),
    path('duration/<str:duration_alias>', chart_views.chart_index_page, name='chart_index_with_duration'),
    path('translator/<str:translator_alias>', chart_views.chart_index_page, name='chart_index_with_translator'),

    path('favorites/add/<str:vn_title>', chart_views.add_favorite_chart, name='chart_favorites_add'),
    path('favorites/remove/<str:vn_title>', chart_views.remove_favorite_chart, name='chart_favorites_remove'),
    path('favorites/genre/<str:genre_alias>', chart_views.chart_favorite_page, name='chart_index_with_genre'),
    path('favorites/tag/<str:tag_alias>', chart_views.chart_favorite_page, name='chart_index_with_tag'),
    path('favorites/studio/<str:studio_alias>', chart_views.chart_favorite_page, name='chart_index_with_studio'),
    path('favorites/staff/<str:staff_alias>', chart_views.chart_favorite_page, name='chart_index_with_staff'),
    path('favorites/duration/<str:duration_alias>', chart_views.chart_favorite_page, name='chart_index_with_duration'),
    path('favorites/translator/<str:translator_alias>', chart_views.chart_favorite_page, name='chart_index_with_translator'),
]
