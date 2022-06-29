from vn_core.models import VisualNovel, VisualNovelStats
from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer


class VNSerializer(ModelSerializer):
	class Meta:
		model = VisualNovel
		fields = ('title', 'alternative_title', 'description', 'date_of_release', 'vndb_id', 'steam_link')


class UserSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'date_joined')


class VNStatsSerializer(ModelSerializer):
	class Meta:
		model = VisualNovelStats
		fields = '__all__'

