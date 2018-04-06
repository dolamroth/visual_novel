from django.urls import path, include

import translation.api.urls

urlpatterns = [
    path('translation/', include(translation.api.urls))
]
