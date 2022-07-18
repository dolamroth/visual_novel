from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from vn_core.models import VisualNovel, VisualNovelStats
from django.contrib.auth.models import User

from .serializers import VNSerializer, UserSerializer, VNStatsSerializer


class VNAPIView(ListModelMixin, GenericViewSet):
	queryset = VisualNovel.objects.all()
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	serializer_class = VNSerializer


class UserAPIView(ListModelMixin, GenericViewSet):
	queryset = User.objects.all()
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	serializer_class = UserSerializer


class VNStatsAPIView(ListModelMixin, GenericViewSet):
	queryset = VisualNovelStats.objects.select_related('visual_novel').only('visual_novel__title', 'rate', 'date').all()
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	serializer_class = VNStatsSerializer


class RemoveTokenAPIView(DestroyModelMixin, GenericViewSet):
	queryset = Token.objects.all()
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]

	def get_object(self):
		return self.queryset.get(user=self.request.user)
