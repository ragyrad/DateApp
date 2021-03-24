from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Profile


class ProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Profile
        fields = ('username', 'first_name', 'email', 'sex', 'sex_looking_for', 'country', 'city', 'date_of_birth')

    def cleaned_date_of_birth(self):
        date_of_birth =  self.cleaned_data['date_of_birth']
        # int(True) = 1, int(False) = 0
        # so if today's month and day is less than the month and day of birth, we subtract 1 from the age
        age = date.today().year - date_of_birth.year - \
              ((date.today().month, date.today().day) < (date_of_birth.month, date_of_birth.day))
        if age < 18:
            raise ValidationError('You must be over 18 years old.')
        return date_of_birth


class ProfileChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'email', 'sex', 'sex_looking_for', 'country', 'city', 'date_of_birth')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('description', 'sex_looking_for',)
