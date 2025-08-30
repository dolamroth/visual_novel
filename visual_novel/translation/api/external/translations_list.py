from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import OuterRef
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from translation.models import TranslationStatisticsChapter, TranslationItem
from core.contrib.postgres.subqueries import SubqueryJsonAgg
from .serializers import TranslationItemResponseSerializer, TranslationItemNestedResponseSerializer
from .authentication import ExternalAPITokenAuthentication


class TranslationListView(APIView):
    serializer_class = TranslationItemResponseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExternalAPITokenAuthentication]

    @swagger_auto_schema(
        operation_summary="Список переводов",
        operation_description="Главы выводятся плоским списком, структура определяется ключами level, parent_id, left_key, right_key (по модели Nested Sets)",
        operation_id="translation_list_flatten",
        responses={
            200: openapi.Response(
                'Список переводов',
                schema=TranslationItemResponseSerializer(many=True),
            ),
            401: openapi.Response("Учетные данные не были предоставлены."),
            403: openapi.Response("У вас недостаточно прав для выполнения данного действия."),
        },
        tags=["Переводы"],
    )
    def get(self, request):
        items_sq = TranslationStatisticsChapter.objects.filter(
            tree_id=OuterRef("statistics__tree_id"),
        ).order_by("lft")

        qs = TranslationItem.objects.select_related(
            "statistics",
            "visual_novel",
            "translator",
        ).filter(
            statistics__isnull=False,
            is_published=True,
        ).annotate(
            items=SubqueryJsonAgg(items_sq),
        )

        return Response(self.serializer_class(qs, many=True).data)


class TranslationListNestedView(TranslationListView):
    serializer_class = TranslationItemNestedResponseSerializer

    @swagger_auto_schema(
        operation_summary="Список переводов (дерево)",
        operation_description="Главы выводятся деревом",
        operation_id="translation_list_tree",
        responses={
            200: openapi.Response(
                'Список переводов',
                schema=TranslationItemNestedResponseSerializer(many=True),
            ),
            401: openapi.Response("Учетные данные не были предоставлены."),
            403: openapi.Response("У вас недостаточно прав для выполнения данного действия."),
        },
        tags=["Переводы"],
    )
    def get(self, request):
        return super().get(request)
