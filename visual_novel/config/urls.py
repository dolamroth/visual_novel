from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.urls import path, include

from django.contrib.auth import views as auth_views
from core import views as core_views
from .views import yandex_view

from core.forms import (
    CustomAuthentificationForm, CustomPasswordResetForm, CustomSetPasswordForm
)

from . import api_urls
import chart.urls
import news.urls
import offer_service.urls
import translation.urls

from core.sitemap import StaticViewsSitemap
from cinfo.sitemap import GenreSitemap, TagSitemap, StudioSitemap, StaffSitemap, TranslatorSitemap
from chart.sitemap import ChartItemSitemap
from translation.sitemap import TranslationItemSitemap

from chart.views import chart_favorite_page, register_rating

from rest_framework.authtoken import views

sitemaps = {
    'static': StaticViewsSitemap,
    'genres': GenreSitemap,
    'tags': TagSitemap,
    'studios': StudioSitemap,
    'staff': StaffSitemap,
    'chart': ChartItemSitemap,
    'translations': TranslationItemSitemap,
    'translators': TranslatorSitemap,
}

urlpatterns = [
    # Admin panel views
    path('admin/', admin.site.urls),

    # debug_toolbar
    path('__debug__/', include('debug_toolbar.urls')),

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
    path('profile/<str:username>', core_views.profile_page, name='profile_page'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemaps'),
    path('robots.txt', TemplateView.as_view(template_name="includes/robots.txt"),
         {'http_domain': settings.VN_HTTP_DOMAIN}, name='robots'),
    path('favicon.ico', core_views.favicon, name='favicon'),
    path('google<str:google_key>.html', core_views.google_site_verification, name='google-site-verification'),
    path('about', TemplateView.as_view(template_name="pages/about.html"), name='about'),

    # Apps views
    path('offers/', include(offer_service.urls)),
    path('translation/', include(translation.urls)),
    path('chart/favorites', chart_favorite_page, name='chart_favorites'),
    path('chart/', include(chart.urls)),
    path('chart/rating/<str:vn_title>/<int:rating>', register_rating, name='rating'),
    path('news/', include(news.urls)),

    path('yandex/', yandex_view, name='yandex_maps'),

    # system_api urls
    path('api-token-auth/', views.obtain_auth_token),
    path('api_vn/', include('system_api.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
