from django.urls import path

from . import views as chart_views

urlpatterns = [
    path(r'<str:vn_alias>', chart_views.chart_page, name='detail_chart'),
    path(r'', chart_views.chart_index_page, name='chart_index'),
    path(r'genre/<str:genre_alias>', chart_views.chart_index_page, name='chart_index_with_genre'),
    path(r'tag/<str:tag_alias>', chart_views.chart_index_page, name='chart_index_with_tag'),
    path(r'studio/<str:studio_alias>', chart_views.chart_index_page, name='chart_index_with_studio'),
    path(r'staff/<str:staff_alias>', chart_views.chart_index_page, name='chart_index_with_staff'),
    path(r'duration/<str:duration_alias>', chart_views.chart_index_page, name='chart_index_with_duration'),
]
