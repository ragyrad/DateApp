from django.db import models

from profiles.models import Profile


class Message(models.Model):
    author = models.ForeignKey(Profile, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    class Meta:
        ordering = ['timestamp']


class Chat(models.Model):
    participants = models.ManyToManyField(Profile, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)

    def get_dialog_participant(self, username):
        """
        A method that returns the user with whom the person is communicating.
        Works for private messages between two people.
        """
        return self.participants.exclude(username=username).first()
