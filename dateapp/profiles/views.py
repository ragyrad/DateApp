from datetime import date

from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProfileCreationForm


class UserRegisterView(View):

    def get(self, request):
        form = ProfileCreationForm()
        return render(request, 'profiles/register.html', {'form': form})

    def post(self, request):
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            return render(request, 'profiles/register_done.html', {'new_user': new_user})


class MyProfileView(View):
    def get(self, request):
        user = request.user
        age = date.today().year - user.date_of_birth.year - \
              ((date.today().month, date.today().day) < (user.date_of_birth.month, user.date_of_birth.day))
        return render(request, 'profiles/my_profile.html', {'user': user, 'age': age})
