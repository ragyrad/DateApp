from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, Photo
from .forms import ProfileCreationForm, ProfileChangeForm


class ProfileAdmin(UserAdmin):
    model = Profile
    add_form = ProfileCreationForm
    form = ProfileChangeForm
    ordering = ('first_name',)
    list_display = ['username', 'first_name', 'email', 'sex', 'country', 'city', 'date_of_birth']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'password1', 'password2', 'email', 'country', 'city',
                       'date_of_birth', 'sex', 'sex_looking_for'),
        }),
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User profile',
            {
                'fields': (
                    'sex',
                    'sex_looking_for',
                    'country',
                    'city',
                    'date_of_birth',
                    'description',
                )
            }
        )
    )


admin.site.register(Profile, ProfileAdmin)

admin.site.register(Photo)