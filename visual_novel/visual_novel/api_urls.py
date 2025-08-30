from django.urls import path, include

import news.api.urls
import translation.api.urls
import translation.api.external.urls

urlpatterns = [
    path('translation/', include(translation.api.urls)),
    path('news/', include(news.api.urls)),
    path('external/translation/', include(translation.api.external.urls)),
]
