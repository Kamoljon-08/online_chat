from rest_framework import serializers
from chat.models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('sender', 'message', 'created_at')