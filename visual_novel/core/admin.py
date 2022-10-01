from django.contrib import admin
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

from translation.models import TranslationSubscription

from .models import Profile


class TranslationSubscriptionInline(admin.TabularInline):
    model = TranslationSubscription
    extra = 3


class ProfileAdmin(admin.ModelAdmin):
    formfield_overrides = {
            BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }
    inlines = (TranslationSubscriptionInline,)
    list_display = (
        '__str__', 'is_staff', 'is_superuser', 'email_confirmed',
    )
    list_filter = (
        'user__is_staff',
    )


admin.site.register(Profile, ProfileAdmin)
