from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include

from django.contrib.auth import views as auth_views
from core import views as core_views

from core.forms import (
    CustomAuthentificationForm, CustomPasswordResetForm, CustomSetPasswordForm
)

from . import api_urls
import chart.urls
import offer_service.urls
import translation.urls

urlpatterns = [
    # Admin panel views
    path('admin/', admin.site.urls),

    # API urls
    path('api/', include(api_urls)),

    # Authentification views
    path('login/', auth_views.LoginView.as_view(
        template_name='pages/login.html',
        form_class=CustomAuthentificationForm,
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='pages/logout.html'
    ), name='logout'),
    path('activate/<str:uidb64>/<str:token>/',
        core_views.activate, name='activate'),
    path('account_activation_sent/', core_views.account_activation_sent, name='account_activation_sent'),
    path('signup/', core_views.signup, name='signup'),

    # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(
        email_template_name='pages/password_reset_email.html',
        form_class=CustomPasswordResetForm,
        template_name='pages/password_reset_form.html',
        subject_template_name='pages/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name = 'pages/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = 'pages/password_reset_confirm.html',
        form_class = CustomSetPasswordForm
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'pages/password_reset_complete.html',
    ), name='password_reset_complete'),

    # Plain pages views
    path('', TemplateView.as_view(template_name="pages/index.html"), name='main'),

    # Apps views
    path('offers/', include(offer_service.urls)),
    path('translation/', include(translation.urls)),
    path('chart/', include(chart.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
