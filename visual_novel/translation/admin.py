from django.contrib import admin

from .models import TranslationItem, TranslationBetaLink


class TranslationBetaLinkInline(admin.TabularInline):
    model = TranslationBetaLink
    extra = 3


class TranslationItemAdmin(admin.ModelAdmin):
    inlines = (TranslationBetaLinkInline,)
    list_display = (
        '__str__', 'is_published', 'visual_novel'
    )
    readonly_fields = ('statistics',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('visual_novel',)
        return self.readonly_fields


admin.site.register(TranslationItem, TranslationItemAdmin)
