from bitfield import BitField

from django.contrib import admin

from .models import TranslationItem, TranslationBetaLink, TranslationItemSendToVK
from .widgets import StatusBitFieldWidget


class TranslationBetaLinkInline(admin.TabularInline):
    model = TranslationBetaLink
    extra = 3

    def get_queryset(self, request):
        qs = super(TranslationBetaLinkInline, self).get_queryset(request)
        return qs.filter(is_published=True)


class TranslationItemAdmin(admin.ModelAdmin):
    inlines = (TranslationBetaLinkInline,)
    list_display = (
        '__str__', 'is_published', 'visual_novel'
    )
    fields = (
        'is_published', 'moderators', 'translator', 'status', 'statistics', 'visual_novel'
    )
    formfield_overrides = {
        BitField: {'widget': StatusBitFieldWidget},
    }
    readonly_fields = ('statistics',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('visual_novel',)
        return self.readonly_fields


admin.site.register(TranslationItem, TranslationItemAdmin)
admin.site.register(TranslationBetaLink)
admin.site.register(TranslationItemSendToVK)
