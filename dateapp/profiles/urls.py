from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'profiles'

urlpatterns = [
    path('', views.MyProfileView.as_view(), name='my_profile'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),
    path('upload-photo/', views.PhotoUploadView.as_view(), name='photo_upload'),
    path('delete-photo/<int:id>', views.PhotoDeleteView.as_view(), name='photo_delete'),
    path('people/', views.ProfileListView.as_view(), name='profiles_list')
]

