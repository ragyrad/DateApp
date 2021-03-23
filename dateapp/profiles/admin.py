from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class PostAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'slug', 'phone', 'country', 'city', 'date_of_birth')
    prepopulated_fieldsa = {'slug': ('id',)}
