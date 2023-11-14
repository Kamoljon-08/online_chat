from django.db import models

# Create your models here.
class ChatMessage(models.Model):
    sender = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

