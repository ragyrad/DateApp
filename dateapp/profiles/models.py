from datetime import date

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    """User model"""
    SEX_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('no_matter', 'No matter'),
    )

    PLACE_CHOICES = (
        ('city', 'My city'),
        ('country', 'My country'),
        ('word', 'All word')
    )

    first_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='male')
    sex_looking_for = models.CharField(max_length=10, choices=SEX_CHOICES, default='female')
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    place_looking_for = models.CharField(max_length=10, choices=PLACE_CHOICES, default='city')
    date_of_birth = models.DateField(default=timezone.now)
    description = models.TextField(max_length=7000, blank=True)

    def get_age(self):
        """Function that calculate age of the user"""
        return date.today().year - self.date_of_birth.year - \
              ((date.today().month, date.today().day) < (self.date_of_birth.month, self.date_of_birth.day))

    class Meta:
        ordering = ('-first_name',)

    def __str__(self):
        return self.first_name


class Photo(models.Model):
    """User photo model """
    profile = models.ForeignKey(Profile, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles_photo')
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
