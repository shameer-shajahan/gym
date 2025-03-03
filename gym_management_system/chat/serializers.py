from rest_framework import serializers
from .models import ChatRoom, Message
from users.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender_details = UserSerializer(source='sender', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'sender', 'sender_details', 'content', 'timestamp', 'is_read']
        read_only_fields = ['timestamp']

class ChatRoomSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    staff_details = UserSerializer(source='staff', read_only=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'user', 'user_details', 'staff', 'staff_details', 'created_at', 'last_message']
        read_only_fields = ['created_at']
    
    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()
        if last_message:
            return {
                'content': last_message.content,
                'timestamp': last_message.timestamp,
                'sender': last_message.sender.id,
                'is_read': last_message.is_read
            }
        return None

class ChatRoomWithMessagesSerializer(ChatRoomSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'user', 'user_details', 'staff', 'staff_details', 'created_at', 'messages']
        read_only_fields = ['created_at']