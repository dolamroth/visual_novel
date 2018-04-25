from django.urls import path, include

import translation.api.urls
import core.api.urls

urlpatterns = [
    path('translation/', include(translation.api.urls)),
    path('core/', include(core.api.urls))
]
