from datetime import date

from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import ProfileCreationForm, ProfileEditForm, UploadPhotoForm
from .models import Photo

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


class PhotoUploadView(View):
    def get(self, request):
        photos = request.user.photos.all()
        form = UploadPhotoForm()
        return render(request, 'profiles/upload_photo.html', {'photos': photos, 'form': form})

    def post(self, request):
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            print('=' * 10 + '\nValid\n' + '=' * 10)
            for f in request.FILES.getlist('photos'):
                data = f.read()  # If the file fits entirely in memory
                photo = Photo(profile=request.user)
                photo.image.save(f.name, ContentFile(data))
                photo.save()
        print('='*10 + '\nInvalid\n' + '='*10)
        return redirect('profiles:photo_upload')


class PhotoDeleteView(View):
    def get(self, request, id):
        image = Photo.objects.get(pk=id)
        image.delete()
        return redirect('profiles:photo_upload')
