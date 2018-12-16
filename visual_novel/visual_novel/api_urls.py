from django.urls import path, include

import news.api.urls
import translation.api.urls

urlpatterns = [
    path('translation/', include(translation.api.urls)),
    path('news/', include(news.api.urls))
]
