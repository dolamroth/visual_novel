from django.contrib import admin

from translation.models import TranslationSubscription

from .models import Profile


class TranslationSubscriptionInline(admin.TabularInline):
    model = TranslationSubscription
    extra = 3


class ProfileAdmin(admin.ModelAdmin):
    inlines = (TranslationSubscriptionInline,)
    list_display = (
        '__str__', 'is_staff', 'is_superuser', 'email_confirmed',
    )
    list_filter = (
        'user__is_staff',
    )


admin.site.register(Profile, ProfileAdmin)
