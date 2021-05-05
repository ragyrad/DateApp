import string
import random
from datetime import date, datetime, timedelta

from django.db import models
from django.utils import timezone
from django.core.cache import cache
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

from cities_light.receivers import connect_default_signals
from cities_light.models import AbstractCountry, AbstractRegion, AbstractSubRegion, AbstractCity

from smart_selects.db_fields import ChainedForeignKey

from dateapp import settings

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class Country(AbstractCountry):
    pass
connect_default_signals(Country)


class Region(AbstractRegion):
    pass
connect_default_signals(Region)


class SubRegion(AbstractSubRegion):
    pass
connect_default_signals(SubRegion)


class City(AbstractCity):
    def __str__(self):
        return f'{self.name}'
connect_default_signals(City)


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

    slug = models.SlugField(max_length=100, unique=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='male')
    sex_looking_for = models.CharField(max_length=10, choices=SEX_CHOICES, default='female')
    email = models.EmailField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = ChainedForeignKey(
        City,
        chained_field='country',
        chained_model_field='country',
        show_all=False,
        null=True,
    )
    place_looking_for = models.CharField(max_length=10, choices=PLACE_CHOICES, default='city')
    date_of_birth = models.DateField(default=timezone.now)
    description = models.TextField(max_length=7000, blank=True)
    relationships = models.ManyToManyField('self' , through='Relationship', symmetrical=False)

    def get_age(self):
        """Function that calculate age of the user"""
        return date.today().year - self.date_of_birth.year - \
              ((date.today().month, date.today().day) < (self.date_of_birth.month, self.date_of_birth.day))

    def last_seen(self):
        return cache.get(f'seen_{self.username}')

    def online(self):
        if self.last_seen():
            now = datetime.now()
            if now > self.last_seen() + timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            return True
        return False

    class Meta:
        ordering = ('-first_name',)

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + '_' + str(self.first_name))
        super(Profile, self).save(*args, **kwargs)


class Photo(models.Model):
    """User photo model """
    profile = models.ForeignKey(Profile, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles_photo')
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']


class Relationship(models.Model):
    user = models.ForeignKey(Profile, related_name='user', on_delete=models.CASCADE)
    target = models.ForeignKey(Profile, related_name='target_user', on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    match = models.BooleanField(default=False)
    match_date = models.DateTimeField(blank=True, null=True)
