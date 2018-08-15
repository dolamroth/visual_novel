from django.contrib import admin

from .models import Studio

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'alias', 'rank_by_visits', )
