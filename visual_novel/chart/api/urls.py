from django.urls import path

from .. import views as chart_views

urlpatterns = [
    path(r'<str:vn_alias>', chart_views.chart_page, name='detail_chart'),
    path(r'', chart_views.chart_index_page, name='chart_index'),
]
