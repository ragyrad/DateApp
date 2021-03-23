from datetime import date

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class Profile(AbstractUser):
    first_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    date_of_birth = models.DateField(default=timezone.now)
    description = models.TextField()

    class Meta:
        ordering = ('first_name',)

    def __str__(self):
        return self.first_name


class Photo(models.Model):
    profile = models.ForeignKey(Profile, related_name='photos', on_delete=models.CASCADE)
    url = models.URLField()
    image = models.ImageField(upload_to='profiles_photo')
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
