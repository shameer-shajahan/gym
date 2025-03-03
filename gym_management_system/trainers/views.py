from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TrainerProfile
from .serializers import TrainerProfileSerializer, TrainerCreateSerializer
from users.models import User

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsTrainerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'trainer'

class TrainerListView(generics.ListAPIView):
    queryset = TrainerProfile.objects.all()
    serializer_class = TrainerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class TrainerDetailView(generics.RetrieveAPIView):
    queryset = TrainerProfile.objects.all()
    serializer_class = TrainerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class TrainerCreateView(generics.CreateAPIView):
    serializer_class = TrainerCreateSerializer
    permission_classes = [IsAdminUser]

class TrainerUpdateView(generics.UpdateAPIView):
    queryset = TrainerProfile.objects.all()
    serializer_class = TrainerProfileSerializer
    permission_classes = [IsAdminUser]

class TrainerDeleteView(generics.DestroyAPIView):
    queryset = TrainerProfile.objects.all()
    permission_classes = [IsAdminUser]
    
    def perform_destroy(self, instance):
        user = instance.user
        instance.delete()
        user.delete()

class TrainerProfileView(APIView):
    permission_classes = [IsTrainerUser]
    
    def get(self, request):
        try:
            trainer_profile = TrainerProfile.objects.get(user=request.user)
            serializer = TrainerProfileSerializer(trainer_profile)
            return Response(serializer.data)
        except TrainerProfile.DoesNotExist:
            return Response(
                {"error": "Trainer profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )