from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chat/index.html')


class RoomView(LoginRequiredMixin, View):
    def get(self, request, room_name):
        return render(request, 'chat/room.html', {'room_name': room_name})
