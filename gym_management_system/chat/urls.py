from django.urls import path
from .views import (
    ChatRoomListView, ChatRoomDetailView, ChatRoomCreateView,
    MessageListView, MessageCreateView, MarkMessagesAsReadView
)

urlpatterns = [
    path('rooms/', ChatRoomListView.as_view(), name='chat-room-list'),
    path('rooms/<int:pk>/', ChatRoomDetailView.as_view(), name='chat-room-detail'),
    path('rooms/create/', ChatRoomCreateView.as_view(), name='chat-room-create'),
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('messages/mark-read/<int:chat_room_id>/', MarkMessagesAsReadView.as_view(), name='mark-messages-read'),
]