from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import VNAPIView, UserAPIView, VNStatsAPIView, RemoveTokenAPIView

app_name = 'system_api'
urlpatterns = [
	path('login', obtain_auth_token, name='login'),
	path('logout', RemoveTokenAPIView.as_view({'delete': 'destroy'}), name='logout'),
	path('vn_list', VNAPIView.as_view({'get': 'list'}), name='nv_list'),
	path('users_list', UserAPIView.as_view({'get': 'list'}), name='users_list'),
	path('vn_stats_list', VNStatsAPIView.as_view({'get': 'list'}), name='vn_stats'),
]
