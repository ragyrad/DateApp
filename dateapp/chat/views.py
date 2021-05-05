from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Chat
from django.views import View


class DialogView(LoginRequiredMixin, View):
    def get(self, request, chat_id):
        user = request.user
        try:
            chat = Chat.objects.get(id=chat_id, participants__in=[user])
        except Chat.DoesNotExist:
            chat = None
        if chat:
            # if request user in chat
            chats = Chat.objects.filter(participants__in=[user])
            participant = chat.get_dialog_participant(user.username)
            return render(request, 'chat/chat.html', {
                'username': user.username,
                'participant': participant,
                'chat': chat,
                'chat_id': chat.id,
                'chats': chats,
            })
        else:
            # redirect to the first chat for this user
            return HttpResponseRedirect(reverse('chat:dialog', args=(request.user.chats.first().id,)))