from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, ChatRoomWithMessagesSerializer, MessageSerializer
from users.models import User

class ChatRoomListView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'user':
            return ChatRoom.objects.filter(user=user)
        elif user.role in ['trainer', 'expert']:
            return ChatRoom.objects.filter(staff=user)
        elif user.role == 'admin':
            return ChatRoom.objects.all()
        return ChatRoom.objects.none()

class ChatRoomDetailView(generics.RetrieveAPIView):
    serializer_class = ChatRoomWithMessagesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'user':
            return ChatRoom.objects.filter(user=user)
        elif user.role in ['trainer', 'expert']:
            return ChatRoom.objects.filter(staff=user)
        elif user.role == 'admin':
            return ChatRoom.objects.all()
        return ChatRoom.objects.none()

class ChatRoomCreateView(generics.CreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        staff_id = request.data.get('staff')
        
        # Check if chat room already exists
        existing_chat = ChatRoom.objects.filter(user_id=user_id, staff_id=staff_id).first()
        if existing_chat:
            serializer = self.get_serializer(existing_chat)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Validate that staff is either trainer or expert
        try:
            staff = User.objects.get(id=staff_id)
            if staff.role not in ['trainer', 'expert']:
                return Response(
                    {"error": "Staff must be a trainer or expert"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                {"error": "Staff user not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return super().create(request, *args, **kwargs)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        chat_room_id = self.request.query_params.get('chat_room')
        if not chat_room_id:
            return Message.objects.none()
        
        user = self.request.user
        try:
            chat_room = ChatRoom.objects.get(id=chat_room_id)
            if user == chat_room.user or user == chat_room.staff or user.role == 'admin':
                return Message.objects.filter(chat_room_id=chat_room_id)
        except ChatRoom.DoesNotExist:
            pass
        
        return Message.objects.none()

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        chat_room_id = self.request.data.get('chat_room')
        try:
            chat_room = ChatRoom.objects.get(id=chat_room_id)
            user = self.request.user
            
            if user != chat_room.user and user != chat_room.staff and user.role != 'admin':
                raise serializers.ValidationError("You don't have permission to send messages in this chat room")
                
            serializer.save(sender=user)
        except ChatRoom.DoesNotExist:
            raise serializers.ValidationError("Chat room not found")

class MarkMessagesAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, chat_room_id):
        try:
            chat_room = ChatRoom.objects.get(id=chat_room_id)
            user = request.user
            
            if user != chat_room.user and user != chat_room.staff and user.role != 'admin':
                return Response(
                    {"error": "You don't have permission to access this chat room"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # Mark all messages from the other user as read
            if user == chat_room.user:
                Message.objects.filter(chat_room=chat_room, sender=chat_room.staff, is_read=False).update(is_read=True)
            else:
                Message.objects.filter(chat_room=chat_room, sender=chat_room.user, is_read=False).update(is_read=True)
                
            return Response({"message": "Messages marked as read"})
        except ChatRoom.DoesNotExist:
            return Response(
                {"error": "Chat room not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )