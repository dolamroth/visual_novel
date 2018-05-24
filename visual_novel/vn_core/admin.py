from django.contrib import admin
from django.utils.html import format_html

from .models import VisualNovel, VNGenre, VNStaff, VNStudio, VNTag


class GenreInline(admin.TabularInline):
    model = VNGenre
    extra = 3


class TagInline(admin.TabularInline):
    model = VNTag
    extra = 3


class StudioInline(admin.TabularInline):
    model = VNStudio
    extra = 3


class StaffInline(admin.TabularInline):
    model = VNStaff
    extra = 3


class VisualNovelAdmin(admin.ModelAdmin):
    def photo_tag(self, obj):
        return format_html('<img src="%s" width="150" height="auto" />' % obj.photo.url if obj.photo else '')

    photo_tag.short_description = 'Фотография'
    photo_tag.allow_tags = True
    inlines = (GenreInline, TagInline, StudioInline, StaffInline, )
    list_display = (
        'title', 'is_published', 'alternative_title', 'photo_tag', 'description', 'date_of_release', 'longevity',
        'vndb_id', 'steam_link', 'alias'
    )
    fields = ('title', 'photo_tag', 'photo', 'alternative_title', 'description', 'date_of_release', 'vndb_id',
              'steam_link', 'longevity', 'alias', 'rate', 'popularity', 'vote_count')
    readonly_fields = ['photo_tag']


admin.site.register(VisualNovel, VisualNovelAdmin)
