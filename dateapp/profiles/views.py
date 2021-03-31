from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django import forms
from .forms import ProfileCreationForm, ProfileEditForm, UploadPhotoForm
from .models import Profile, Photo


class UserRegisterView(View):
    """View for user registration"""
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
        return render(request, 'profiles/register.html', {'form': form})


class MyProfileView(LoginRequiredMixin, View):
    """View for user profile where he can change the description and the gender he is looking for"""
    def get(self, request):
        user = request.user
        age = user.get_age()
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


class PhotoUploadView(LoginRequiredMixin, View):
    """View where user can upload profile photos"""
    def get(self, request):
        photos = request.user.photos.all()
        form = UploadPhotoForm()
        return render(request, 'profiles/upload_photo.html', {'photos': photos, 'form': form})

    def post(self, request):
        form = UploadPhotoForm(request.POST, request.FILES)
        user_photos = request.user.photos.all()
        # User can have a maximum of 8 photos
        if len(user_photos) + len(request.FILES.getlist('photos')) > 8:
            form.add_error('photos', forms.ValidationError('You can have a maximum of 8 photos.'))

        if form.is_valid():
            for f in request.FILES.getlist('photos'):
                data = f.read()  # If the file fits entirely in memory
                photo = Photo(profile=request.user)
                photo.image.save(f.name, ContentFile(data))
                photo.save()
            return redirect('profiles:photo_upload')
        return render(request, 'profiles/upload_photo.html', {'photos': user_photos, 'form': form})


class PhotoDeleteView(LoginRequiredMixin, View):
    """View where user can delete profile photos"""
    def get(self, request, id):
        image = Photo.objects.get(pk=id)
        image.delete()
        return redirect('profiles:photo_upload')


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    paginate_by = 1
    context_object_name = 'profiles'

    def get_queryset(self):
        sex_filter = self.request.user.sex_looking_for
        queryset = Profile.objects.all().exclude(id=self.request.user.id)
        if sex_filter != 'no_matter':
            queryset = queryset.filter(sex=sex_filter)
        return queryset