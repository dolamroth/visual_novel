import math

from constance import config

from django.http import JsonResponse

from ..models import News
from ..serializers import NewsSerializer

DEFAULT_NEWS_START_PAGE = 1


def get_news_list(request):
    news_per_page = config.NEWS_PER_PAGE
    news_start_page = request.GET.get('start_page', DEFAULT_NEWS_START_PAGE)

    try:
        news_start_page = int(news_start_page)
    except ValueError:
        return JsonResponse({})

    query = """
            select * 
            from {db_table}
            where is_published is true
            order by created_at desc
            limit {limit} 
            offset {offset}
        """.format(
        db_table=News._meta.db_table,
        limit=news_per_page,
        offset=(news_start_page - 1) * news_per_page if news_start_page > 0 else 0
    )

    all_news = News.objects.raw(query)
    all_news_orm = News.objects.filter(is_published=True)
    all_news_count = all_news_orm.count()

    total_pages = int(math.ceil(all_news_count / news_per_page))
    # Обрезка по максимальной и минимальной страницам
    if news_start_page < 1:
        news_start_page = 1
    if (news_start_page - 1) * news_per_page >= all_news_count:
        news_start_page = total_pages

    context = dict()
    context['has_previous_page'] = (news_start_page > 1)
    context['has_next_page'] = (news_start_page < total_pages)
    context['current_page'] = news_start_page
    context['total_pages'] = total_pages
    context['total_news'] = all_news_count

    news_serialized = NewsSerializer(all_news, many=True)
    context['news'] = news_serialized.data

    # Pagination
    context['pagination'] = list()
    context['pagination'].append({'page': 1, 'active': (news_start_page == 1), 'link': True})
    if (total_pages > 1):
        context['pagination'].append({'page': 2, 'active': (news_start_page == 2), 'link': True})

    if (news_start_page > 6):
        context['pagination'].append({'page': None, 'active': False, 'link': False})
        context['pagination'].append({'page': news_start_page - 3, 'active': False, 'link': True})
        context['pagination'].append({'page': news_start_page - 2, 'active': False, 'link': True})
        context['pagination'].append({'page': news_start_page - 1, 'active': False, 'link': True})
        context['pagination'].append({'page': news_start_page, 'active': True, 'link': True})
    else:
        for i in range(3, news_start_page + 1):
            context['pagination'].append({'page': i, 'active': i == news_start_page, 'link': True})

    if (total_pages - news_start_page > 5):
        if (news_start_page > 1):
            context['pagination'].append({'page': news_start_page + 1, 'active': False, 'link': True})
        context['pagination'].append({'page': news_start_page + 2, 'active': False, 'link': True})
        context['pagination'].append({'page': news_start_page + 3, 'active': False, 'link': True})
        context['pagination'].append({'page': None, 'active': False, 'link': False})
    else:
        ai = 2 if (news_start_page == 1) else 1
        for i in range(news_start_page + ai, total_pages - 1):
            context['pagination'].append({'page': i, 'active': i == news_start_page, 'link': True})

    if (total_pages > 3) and (news_start_page < total_pages - 1):
        context['pagination'].append(
            {'page': total_pages - 1, 'active': (news_start_page == total_pages - 1), 'link': True})
    if (total_pages > 2) and (news_start_page < total_pages):
        context['pagination'].append({'page': total_pages, 'active': (news_start_page == total_pages), 'link': True})

    return JsonResponse(context)
