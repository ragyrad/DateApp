from datetime import date

from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView

from .forms import ProfileCreationForm, ProfileEditForm


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
        form = ProfileEditForm(initial={'description': user.description, 'sex_looking_for': user.sex_looking_for})
        return render(request, 'profiles/my_profile.html', {'form': form, 'user': user, 'age': age})

    def post(self, request):
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            temp_user = form.save(commit=False)
            request.user.description = temp_user.description
            request.user.sex_looking_for = temp_user.sex_looking_for
            request.user.save()
            return redirect('profiles:my_profile')
