import arrow
import pytz

from collections import OrderedDict

from django.conf import settings
from django.db import models

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.relations import PKOnlyObject

from ..models import TranslationItem, TranslationStatisticsChapter
from ..utils import get_status_tuple_for_translation_item


class AddTranslationChapterPartSerializer(serializers.Serializer):
    translation_item_id = serializers.IntegerField()
    new_parent = serializers.IntegerField(min_value=0)
    new_move_to = serializers.CharField()
    title = serializers.CharField(min_length=1, max_length=50)
    script_title = serializers.CharField(max_length=50)
    timezone = serializers.SerializerMethodField()
    is_chapter = serializers.BooleanField(default=False)

    def get_timezone(self, obj):
        user = self.context['user']
        if hasattr(user, 'profile') and user.profile.timezone:
            return user.profile.timezone
        else:
            return settings.DEFAULT_TIME_ZONE


class AddTranslationChapterSerializer(AddTranslationChapterPartSerializer):
    total = serializers.IntegerField(min_value=1)
    new_translated = serializers.IntegerField(min_value=0)
    new_edited_first_pass = serializers.IntegerField(min_value=0)
    new_edited_second_pass = serializers.IntegerField(min_value=0)
    is_chapter = serializers.BooleanField(default=True)


class TranslationChapterPartSerializer(AddTranslationChapterPartSerializer):
    translation_chapter_id = serializers.IntegerField()


class TranslationChapterSerializer(AddTranslationChapterSerializer):
    translation_chapter_id = serializers.IntegerField()


class StatisticsDescription(serializers.Serializer):
    description = serializers.CharField(max_length=500, allow_blank=True)


class StatisticsComment(serializers.Serializer):
    comment = serializers.CharField(max_length=2000, allow_blank=True)


class BetaLinkSerializer(serializers.Serializer):
    translation_item_id = serializers.IntegerField(min_value=1)
    title = serializers.CharField(min_length=1, max_length=50)
    comment = serializers.CharField(max_length=2000, allow_blank=True)
    url = serializers.CharField(min_length=1, max_length=200)
    betalink_id = serializers.IntegerField(min_value=0)
    timezone = serializers.SerializerMethodField()

    def get_timezone(self, obj):
        user = self.context['user']
        if hasattr(user, 'profile') and user.profile.timezone:
            return user.profile.timezone
        else:
            return settings.DEFAULT_TIME_ZONE


class TranslationListShortSerializer(serializers.Serializer):

    def __init__(self, instance=None, data=empty, **kwargs):
        super(TranslationListShortSerializer, self).__init__(instance=instance, data=data, **kwargs)
        self.visual_novel = None
        self.statistics = None
        self.total = None
        self.status_tuple = None

    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields

        ##########################################################
        ########## Custom local variables to serializer ##########
        ##########################################################
        self.visual_novel = instance.visual_novel
        self.translation_statistics = instance.statistics
        self.statistics = TranslationStatisticsChapter.objects.get(
            tree_id=(self.translation_statistics).tree_id,
            lft=1
        )
        self.total = (self.statistics).total_rows if (self.statistics).total_rows > 0 else 1
        self.status_tuple = get_status_tuple_for_translation_item(instance)
        ##########################################################
        ########## Custom local variables to serializer ##########
        ##########################################################

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret

    class Meta:
        model = TranslationItem
        fields = (
            'title', 'alias', 'total_rows', 'translated', 'edited_first_pass', 'edited_second_pass', 'translated_perc',
            'edited_first_pass_perc', 'edited_second_pass_perc', 'status_name', 'status_style', 'last_update'
        )

    title = serializers.SerializerMethodField()
    alias = serializers.SerializerMethodField()
    total_rows = serializers.SerializerMethodField()
    translated = serializers.SerializerMethodField()
    edited_first_pass = serializers.SerializerMethodField()
    edited_second_pass = serializers.SerializerMethodField()
    translated_perc = serializers.SerializerMethodField()
    edited_first_pass_perc = serializers.SerializerMethodField()
    edited_second_pass_perc = serializers.SerializerMethodField()
    status_name = serializers.SerializerMethodField()
    status_style = serializers.SerializerMethodField()
    last_update = serializers.SerializerMethodField()

    def get_title(self, obj):
        return (self.visual_novel).title

    def get_alias(self, obj):
        return (self.visual_novel).alias

    def get_total_rows(self, obj):
        return (self.statistics).total_rows

    def get_translated(self, obj):
        return (self.statistics).translated

    def get_edited_first_pass(self, obj):
        return (self.statistics).edited_first_pass

    def get_edited_second_pass(self, obj):
        return (self.statistics).edited_second_pass

    def get_translated_perc(self, obj):
        return "{0:.2f}%".format((self.statistics).translated / self.total * 100.0)

    def get_edited_first_pass_perc(self, obj):
        return "{0:.2f}%".format((self.statistics).edited_first_pass / self.total * 100.0)

    def get_edited_second_pass_perc(self, obj):
        return "{0:.2f}%".format((self.statistics).edited_second_pass / self.total * 100.0)

    def get_last_update(self, obj):
        user = self.context['user']
        user_timezone = pytz.timezone(settings.DEFAULT_TIME_ZONE) \
            if not hasattr(user, 'profile') \
            else user.profile.timezone
        return arrow.get(((self.translation_statistics).last_update)
                                .replace(tzinfo=pytz.utc)).to(user_timezone).datetime.strftime("%Y-%m-%d %H:%M")

    def get_status_name(self, obj):
        return (self.status_tuple).name

    def get_status_style(self, obj):
        return (self.status_tuple).style
