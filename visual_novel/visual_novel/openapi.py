from django.conf import settings

from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class APIExternalOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_paths(self, endpoints, components, request, public):
        paths, prefix = super().get_paths(endpoints, components, request, public)
        paths_dict = {'/api/' + d.lstrip('/'): paths[d] for d in paths}
        return openapi.Paths(paths=paths_dict), '/'

    def should_include_endpoint(self, path, method, view, public):
        return path.startswith("/external")


schema_view = get_schema_view(
    openapi.Info(
        title="Чарт визуальных новелл: внешнее API",
        default_version='v1.0',
    ),
    public=False,
    permission_classes=[permissions.AllowAny, ],
    url=settings.VN_HTTP_DOMAIN,
    urlconf='visual_novel.api_urls',
    generator_class=APIExternalOpenAPISchemaGenerator,
)
