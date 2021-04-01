from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'profiles'

urlpatterns = [
    path('', views.MyProfileView.as_view(), name='my_profile'),

    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),

    # password change urls
    path('password_change/',
         auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('profiles:password_change_done')),
         name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # password reset urls
    path('password_reset/',
         auth_views.PasswordResetView.as_view(success_url=reverse_lazy('profiles:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('profiles:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('upload_photo/', views.PhotoUploadView.as_view(), name='photo_upload'),
    path('delete_photo/<int:id>', views.PhotoDeleteView.as_view(), name='photo_delete'),
    path('people/', views.ProfileListView.as_view(), name='profiles_list'),
    path('like/<int:user_id>', views.LikeView.as_view(), name='like'),
    path('skip/<int:user_id>', views.LikeView.as_view(), name='skip'),
]

