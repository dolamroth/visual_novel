from django.urls import path, include

import core.api.urls
import news.api.urls
import translation.api.urls

urlpatterns = [
    path('translation/', include(translation.api.urls)),
    path('core/', include(core.api.urls)),
    path('news/', include(news.api.urls))
]
