from datetime import timedelta

from django import forms
from django.utils import timezone
from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from notifications.signals import notify

from .tasks import reset_like
from .forms import ProfileCreationForm, ProfileEditForm, UploadPhotoForm
from .models import Profile, Photo, Relationship
from chat.models import Chat


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
    """View for user profile where he can change the description, the gender he is looking for and the location"""
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
            request.user.place_looking_for = temp_user.place_looking_for
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


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    paginate_by = 1
    context_object_name = 'profiles'

    def get_queryset(self):
        user = self.request.user
        user_rlts = [target.target.username for target in Relationship.objects.filter(user=user)]
        queryset = Profile.objects.all().exclude(id=user.id).exclude(username__in=user_rlts)

        # filter by gender
        sex_filter = user.sex_looking_for
        if sex_filter != 'no_matter':
            queryset = queryset.filter(sex=sex_filter)

        # filter by place
        place_filter = user.place_looking_for
        if place_filter != 'word':
            queryset = queryset.filter(country=user.country)
            if place_filter == 'city':
                queryset = queryset.filter(city=user.city)
        return queryset


def create_match(user, target):
    user_rlts = Relationship.objects.filter(user=user, target=target).first()
    target_rlst = Relationship.objects.filter(user=target, target=user).first()
    user_rlts.match = True
    user_rlts.match_date = timezone.now()
    target_rlst.match = True
    target_rlst.match_date = timezone.now()
    user_rlts.save()
    target_rlst.save()


def create_chat(user, target):
    chat = Chat.objects.create()
    chat.participants.add(user)
    chat.participants.add(target)
    chat.save()


def delete_chat(user, target):
    chat = Chat.objects.filter(participants__in=[user]).filter(participants__in=[target]).first()
    for message in chat.messages.all():
        message.delete()
    chat.delete()


class LikeView(LoginRequiredMixin, View):
    def get(self, request, slug):
        target_user = Profile.objects.get(slug=slug)
        # Like the user
        request.user.relationships.add(target_user, through_defaults={'like': True})
        # If the like is mutual, then we make a match
        if Relationship.objects.filter(user=target_user, target=request.user, like=True):
            create_match(request.user, target_user)
            create_chat(request.user, target_user)
            # send notification about match
            notify.send(request.user, recipient=target_user, verb=f'You have a new match with:')
            notify.send(target_user, recipient=request.user, verb=f'You have a new match with:')

        # delete the like in a week if it is not mutual
        week_after = timezone.now() + timedelta(weeks=1)
        reset_like.apply_async((request.user.id, target_user.id), eta=week_after)

        return redirect('profiles:profiles_list')


class SkipView(LoginRequiredMixin, View):
    def get(self, request, slug):
        target_user = Profile.objects.get(slug=slug)
        request.user.relationships.add(target_user)
        return redirect('profiles:profiles_list')


class MatchListView(LoginRequiredMixin, ListView):
    model = Relationship
    paginate_by = 15
    context_object_name = 'matches'
    template_name = 'profiles/match_list.html'

    def get_queryset(self):
        user = self.request.user
        user_matches = Relationship.objects.filter(user=user, match=True)
        return user_matches


class MatchDeleteView(LoginRequiredMixin, View):
    """View delete match for both users"""
    def get(self, request, slug):
        user = request.user
        target = Profile.objects.get(slug=slug)
        rels = Relationship.objects.filter(user__in=[user.id, target.id], target__in=[user.id, target.id], match=True)
        for rel in rels:
            rel.delete()
        # and delete chat between these users
        delete_chat(user, target)
        return redirect('profiles:matches')