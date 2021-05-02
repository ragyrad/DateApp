from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Chat


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chat/index.html')


class RoomView(LoginRequiredMixin, View):
    def get(self, request, room_name):
        return render(request, 'chat/room.html', {'room_name': room_name, 'username': request.user.username})


class DialogView(LoginRequiredMixin, View):
    def get(self, request, chat_id):
        user = request.user
        chat = Chat.objects.get(id=chat_id, participants__in=[user])
        if chat:
            # if request user in chat
            chats = Chat.objects.filter(participants__in=[user])
            participant = chat.get_dialog_participant(user.username)
            return render(request, 'chat/room.html', {
                'username': user.username,
                'participant': participant,
                'chat': chat,
                'chat_id': chat.id,
                'chats': chats,
            })
        else:
            # FIXME: redirect to last dialog for user
            pass