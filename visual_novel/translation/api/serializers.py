from django.conf import settings

from rest_framework import serializers


class TranslationChapterSerializer(serializers.Serializer):
    translation_item_id = serializers.IntegerField()
    translation_chapter_id = serializers.IntegerField()
    total = serializers.IntegerField(min_value=1)
    new_translated = serializers.IntegerField(min_value=0)
    new_edited_first_pass = serializers.IntegerField(min_value=0)
    new_edited_second_pass = serializers.IntegerField(min_value=0)
    new_parent = serializers.IntegerField(min_value=0)
    new_move_to = serializers.CharField()
    title = serializers.CharField(min_length=1, max_length=50)
    script_title = serializers.CharField(min_length=1, max_length=50)
    timezone = serializers.SerializerMethodField()
    is_chapter = serializers.SerializerMethodField()

    def get_timezone(self, obj):
        user = self.context['user']
        if hasattr(user, 'profile') and user.profile.timezone:
            return user.profile.timezone
        else:
            return settings.DEFAULT_TIME_ZONE

    def get_is_chapter(self, obj):
        return self.context['chapter'] == 'True'
