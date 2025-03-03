from django.contrib import admin
from .models import ChatRoom, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'staff', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'staff__email')
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat_room', 'sender', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('content', 'sender__email')