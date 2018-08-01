import arrow
import pytz

from django.conf import settings

from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.Serializer):
    alias = serializers.CharField()
    title = serializers.CharField()
    short_description = serializers.CharField()
    description = serializers.CharField()
    poster_url = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ('alias', 'title', 'short_description', 'description', 'poster_url', 'author', 'created_at', )

    def get_poster_url(self, obj):
        if obj.poster and obj.poster.url:
            return obj.poster.url
        return None

    def get_author(self, obj):
        return obj.author.username

    def get_created_at(self, obj):
        user = self.context.get('user', None)
        if user and hasattr(request.user, 'profile'):
            user_timezone = request.user.profile.timezone
        else:
            user_timezone = pytz.timezone(settings.DEFAULT_TIME_ZONE)
        return arrow.get(
            (obj.created_at).replace(tzinfo=pytz.utc)
        ).to(user_timezone).datetime.strftime("%Y-%m-%d %H:%M:%S")

