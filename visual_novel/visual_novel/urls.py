from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import path, include

import offer_service.urls
import chart.urls

from core.forms import CustomAuthentificationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.login, {
        'template_name': 'pages/login.html',
        'redirect_authenticated_user': True,
        'authentication_form': CustomAuthentificationForm,
    }, name='login'),
    path('logout/', auth_views.logout, {
        'template_name': 'pages/logout.html',
    }, name='logout'),
    path('', TemplateView.as_view(template_name="pages/index.html"), name='main'),
    path('offers/', include(offer_service.urls), name='offers'),
    path('chart/', include(chart.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
