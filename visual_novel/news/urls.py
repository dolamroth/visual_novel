from django.urls import path

from . import views as news_views

urlpatterns = [
    path(r'all', news_views.news_list, name='news_list'),
    path(r'<str:alias>', news_views.get_news, name='news_item'),
]
