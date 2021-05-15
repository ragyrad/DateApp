from .models import Chat


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