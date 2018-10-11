import os

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.relations import PKOnlyObject

from django.conf import settings

from .models import ChartItem


class ChartItemGenreSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        super(ChartItemGenreSerializer, self).__init__(instance=instance, data=data, **kwargs)
        self.description = None

    class Meta:
        fields = ('title', 'description', 'alias', 'link', 'has_description')

    title = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    has_description = serializers.SerializerMethodField()
    alias = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.genre.title

    def get_link(self, obj):
        return os.path.join('/chart/', 'genre', obj.genre.alias)

    def get_description(self, obj):
        self.description = obj.genre.description
        return self.description

    def get_has_description(self, obj):
        return not not self.description

    def get_alias(self, obj):
        return obj.genre.alias


class ChartItemStudioSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        super(ChartItemStudioSerializer, self).__init__(instance=instance, data=data, **kwargs)
        self.description = None

    class Meta:
        fields = ('title', 'description', 'alias', 'link', 'has_description')

    title = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    has_description = serializers.SerializerMethodField()
    alias = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.studio.title

    def get_link(self, obj):
        return os.path.join('/chart/', 'studio', obj.studio.alias)

    def get_description(self, obj):
        self.description = obj.studio.description
        return self.description

    def get_has_description(self, obj):
        return not not self.description

    def get_alias(self, obj):
        return obj.studio.alias


class ChartItemListSerializer(serializers.Serializer):

    class Meta:
        model = ChartItem
        fields = ('title', 'poster_url', 'description', 'alias', 'genres', 'vndb_id', 'vndb_id', 'chart_link',
                  'vndb_mark', 'vndb_popularity', 'studios', )

    title = serializers.SerializerMethodField()
    poster_url = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    alias = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    vndb_id = serializers.SerializerMethodField()
    chart_link = serializers.SerializerMethodField()
    vndb_mark = serializers.SerializerMethodField()
    vndb_popularity = serializers.SerializerMethodField()
    studios = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.visual_novel.title

    def get_poster_url(self, obj):
        return settings.POSTER_STOPPER_URL if not obj.visual_novel.photo else obj.visual_novel.photo.url

    def get_description(self, obj):
        return obj.visual_novel.description

    def get_alias(self, obj):
        return obj.visual_novel.alias

    def get_vndb_id(self, obj):
        return obj.visual_novel.vndb_id

    def get_chart_link(self, obj):
        return os.path.join('/chart/', obj.visual_novel.alias)

    def get_vndb_mark(self, obj):
        return obj.visual_novel.get_rate()

    def get_vndb_popularity(self, obj):
        return obj.visual_novel.get_popularity()

    def get_genres(self, obj):
        return ChartItemGenreSerializer(
            obj.visual_novel.vngenre_set.all().order_by('-weight'),
            many=True
        ).data

    def get_studios(self, obj):
        return ChartItemStudioSerializer(
            obj.visual_novel.vnstudio_set.all().order_by('-weight'),
            many=True
        ).data
