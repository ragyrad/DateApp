import os
from datetime import date, timedelta

from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Profile, Photo
from .forms import ProfileCreationForm


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Profile.objects.create(first_name='Nick', email='nick@ex.com', country='Russia', city='Moscow',
                               date_of_birth='2000-10-10', description='Hi, I\'m Nick')

    def test_first_name_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label,'first name')

    def test_sex_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('sex').verbose_name
        self.assertEquals(field_label,'sex')

    def test_sex_looking_for_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('sex_looking_for').verbose_name
        self.assertEquals(field_label,'sex looking for')

    def test_email_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('email').verbose_name
        self.assertEquals(field_label,'email')

    def test_country_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('country').verbose_name
        self.assertEquals(field_label,'country')

    def test_city_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('city').verbose_name
        self.assertEquals(field_label,'city')

    def test_date_of_birth_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label,'date of birth')

    def test_description_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('description').verbose_name
        self.assertEquals(field_label,'description')

    def test_first_name_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 50)

    def test_sex_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('sex').max_length
        self.assertEquals(max_length, 10)

    def test_sex_looking_for_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('sex_looking_for').max_length
        self.assertEquals(max_length, 10)

    def test_country_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('country').max_length
        self.assertEquals(max_length, 30)

    def test_city_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('city').max_length
        self.assertEquals(max_length, 30)

    def test_description_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('description').max_length
        self.assertEquals(max_length, 7000)

    def test_object_name_is_first_name(self):
        profile = Profile.objects.get(id=1)
        expected_object_name = f'{profile.first_name}'
        self.assertEquals(expected_object_name, str(profile))

    def test_sex_default_value(self):
        profile = Profile.objects.get(id=1)
        expected_default_value = profile.sex
        self.assertEquals(expected_default_value, 'male')

    def test_sex_looking_for_default_value(self):
        profile = Profile.objects.get(id=1)
        expected_default_value = profile.sex_looking_for
        self.assertEquals(expected_default_value, 'female')


class PhotoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Profile.objects.create(first_name='Nick', email='nick@ex.com', country='Russia', city='Moscow',
                               date_of_birth='2000-10-10', description='Hi, I\'m Nick')
        image_path = os.path.join(settings.BASE_DIR, "static/img/default-user-avatar.png")
        Photo.objects.create(profile=Profile.objects.get(id=1),
                             image=SimpleUploadedFile(name='test_image.jpg',
                                                      content=open(image_path, 'rb').read(), content_type='image'))

    def test_profile_label(self):
        photo = Photo.objects.get(id=1)
        field_label = photo._meta.get_field('profile').verbose_name
        self.assertEquals(field_label, 'profile')

    def test_image_label(self):
        photo = Photo.objects.get(id=1)
        field_label = photo._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'image')

    def test_created_label(self):
        photo = Photo.objects.get(id=1)
        field_label = photo._meta.get_field('created').verbose_name
        self.assertEquals(field_label, 'created')


class ProfileCreationFormTest(TestCase):

    def test_profile_creation_form_date_of_birth_in_future(self):
        tomorrow_date = date.today() + timedelta(days=1)
        form_data = {'date_of_birth': tomorrow_date}
        form = ProfileCreationForm(data=form_data)
        self.assertIn('date_of_birth', form.errors)
        self.assertEquals(form.errors['date_of_birth'][0], 'Invalid date - date of birth in the future.')

    def test_profile_creation_form_date_of_birth_user_under_18(self):
        under_18_date = (date.today().year - 18, date.today().month, date.today().day + 1)
        form_data = {'date_of_birth': date(*under_18_date)}
        form = ProfileCreationForm(data=form_data)
        self.assertIn('date_of_birth', form.errors)
        self.assertEquals(form.errors['date_of_birth'][0], 'You must be over 18 years old.')

    def test_profile_creation_form_date_of_birth_normal(self):
        date_of_birth_adult = (date.today().year - 18, date.today().month, date.today().day)
        form_data = {'date_of_birth': date(*date_of_birth_adult)}
        form = ProfileCreationForm(data=form_data)
        self.assertNotIn('date_of_birth', form.errors)
