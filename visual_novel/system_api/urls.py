from django.urls import path

from .views import VNAPIView, UserAPIView, VNStatsAPIView

urlpatterns = [
	path('vn_list', VNAPIView.as_view({'get': 'list'})),
	path('users_list', UserAPIView.as_view({'get': 'list'})),
	path('vn_stats_list', VNStatsAPIView.as_view({'get': 'list'})),
]
