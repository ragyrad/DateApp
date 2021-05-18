from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Profile


class ProfileCreationForm(UserCreationForm):
    """User registration form"""

    class Meta(UserCreationForm.Meta):
        model = Profile
        fields = ('username', 'first_name', 'email', 'sex', 'sex_looking_for', 'country', 'city', 'date_of_birth')

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date.today() < date_of_birth:
            raise forms.ValidationError('Invalid date - date of birth in the future.')
        # int(True) = 1, int(False) = 0
        # so if today's month and day is less than the month and day of birth, we subtract 1 from the age
        age = date.today().year - date_of_birth.year - \
              ((date.today().month, date.today().day) < (date_of_birth.month, date_of_birth.day))
        if age < 18:
            raise forms.ValidationError('You must be over 18 years old.')
        return date_of_birth


class ProfileChangeForm(UserChangeForm):
    """User change data form"""

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'email', 'sex', 'sex_looking_for', 'country', 'city', 'date_of_birth')


class ProfileEditForm(forms.ModelForm):
    """A form so that the user can change the description, search gender, and location"""

    class Meta:
        model = Profile
        fields = ('description', 'min_age_looking_for', 'max_age_looking_for', 'sex_looking_for', 'place_looking_for')


class UploadPhotoForm(forms.Form):
    """Form so that the user can upload the photo for profile"""
    photos = forms.ImageField(widget=forms.FileInput(attrs={'multiple': 'multiple'}))
