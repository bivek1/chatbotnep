from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ChatBot(models.Model):
    of_user = models.ForeignKey(User, related_name="chat_user", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class FAQ(models.Model):
    chatbot = models.ForeignKey(ChatBot, related_name="chat_bot", on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question



