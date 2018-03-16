from django.urls import path

from . import views

urlpatterns = [
    path(r'<str:vn_alias>', views.ChartView.as_view(), name='detail_chart'),
]
