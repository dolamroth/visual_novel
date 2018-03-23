from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include

from django.contrib.auth import views as auth_views
from core import views as core_views

from core.forms import CustomAuthentificationForm

import offer_service.urls
import chart.urls

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
    path('activate/<str:uidb64>/<str:token>/',
        core_views.activate, name='activate'),
    path('account_activation_sent/', core_views.account_activation_sent, name='account_activation_sent'),
    path('signup/', core_views.signup, name='signup'),
    path('', TemplateView.as_view(template_name="pages/index.html"), name='main'),
    path('offers/', include(offer_service.urls), name='offers'),
    path('chart/', include(chart.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
