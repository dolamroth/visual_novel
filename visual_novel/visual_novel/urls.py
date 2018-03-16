from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from chart import views as chart_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="pages/index.html"), name='main'),
    path('chart/', chart_views.chart_index_page, name='chart_main')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
