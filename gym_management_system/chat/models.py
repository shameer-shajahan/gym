from django.db import models
from users.models import User

class ChatRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_chat_rooms')
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chat between {self.user.get_full_name()} and {self.staff.get_full_name()}"

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.sender.get_full_name()} at {self.timestamp}"
    
    class Meta:
        ordering = ['timestamp']