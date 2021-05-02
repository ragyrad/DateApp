from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('<str:room_name>/', views.RoomView.as_view(), name='room'),
    path('<int:chat_id>/', views.DialogView.as_view(), name='dialog'),
]