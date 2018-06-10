from django.http import Http404
from django.shortcuts import render

from .models import News
from .serializers import NewsSerializer


def get_news(request, alias):
    try:
        news = News.objects.get(alias=alias, is_published=True)
    except News.DoesNotExist:
        raise Http404
    return render(request, 'news/news_item.html', context=NewsSerializer(news).data)
