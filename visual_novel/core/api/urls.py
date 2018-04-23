from django.urls import path

from . import views as core_api_views


urlpatterns = [
    path(r'<str:username>/subscriptions_edit', core_api_views.update_subscription_time, name='subscriptions_edit'),
]
