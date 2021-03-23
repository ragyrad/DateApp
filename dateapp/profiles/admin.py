from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile
from .forms import ProfileCreationForm, ProfileChangeForm


class ProfileAdmin(UserAdmin):
    model = Profile
    add_form = ProfileCreationForm
    form = ProfileChangeForm
    ordering = ('first_name',)
    list_display = ['first_name', 'slug', 'phone', 'country', 'city', 'date_of_birth']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'password1', 'password2', 'slug', 'phone', 'country', 'city', 'date_of_birth'),
        }),
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User profile',
            {
                'fields': (
                    'phone',
                    'country',
                    'city',
                    'date_of_birth',
                )
            }
        )
    )


admin.site.register(Profile, ProfileAdmin)