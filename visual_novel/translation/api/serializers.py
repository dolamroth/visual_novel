from django.conf import settings

from rest_framework import serializers


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
    description = serializers.CharField(max_length=500)


class StatisticsComment(serializers.Serializer):
    comment = serializers.CharField(max_length=2000)


class BetaLinkSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=50)
    comment = serializers.CharField(max_length=2000)
    comment = serializers.CharField(min_length=1, max_length=200)
