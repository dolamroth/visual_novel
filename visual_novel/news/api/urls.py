from django.urls import path

from . import views as news_views

urlpatterns = [
    path(r'all', news_views.get_news_list, name='get_news_list'),
]
