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

    class Meta:
        model = News
        fields = ('alias', 'title', 'short_description', 'description', 'poster_url', 'author', )

    def get_poster_url(self, obj):
        if obj.poster and obj.poster.url:
            return obj.poster.url
        return None

    def get_author(self, obj):
        return obj.author.username
