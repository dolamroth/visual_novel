from django.contrib import admin

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
    inlines = (GenreInline, TagInline, StudioInline, StaffInline, )
    list_display = (
        'title', 'alternative_title', 'photo', 'description', 'date_of_release', 'longevity',
        'vndb_id', 'steam_link', 'alias'
    )


admin.site.register(VisualNovel, VisualNovelAdmin)
