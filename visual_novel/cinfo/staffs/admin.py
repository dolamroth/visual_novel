from django.contrib import admin

from .models import Staff

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('title', 'alias', 'rank_by_visits', )
