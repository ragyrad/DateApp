import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Chat, Message
from profiles.models import Profile


class ChatConsumer(WebsocketConsumer):

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result


    def fetch_messages(self, data):
        self.chat = Chat.objects.get(id=int(self.chat_id))

        messages = self.chat.messages.all()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_profile = Profile.objects.filter(username=author).first()

        message = Message.objects.create(
            author=author_profile,
            content=data['message'],
        )
        self.chat.messages.add(message)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_id = f'chat_{self.chat_id}'

        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_id,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        # leave from group
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_id,
            self.channel_name
        )

    def receive(self, text_data):
        """Receive message from WebSocket"""
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # send message to group
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_id,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        """Receive message from room group"""
        message = event['message']
        # send message to WebSocket
        self.send(text_data=json.dumps(message))