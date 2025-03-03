from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import HealthDetail
from .serializers import HealthDetailSerializer

class IsAdminOrTrainerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'trainer']

class HealthDetailListView(generics.ListAPIView):
    queryset = HealthDetail.objects.all()
    serializer_class = HealthDetailSerializer
    permission_classes = [IsAdminOrTrainerUser]

class HealthDetailDetailView(generics.RetrieveAPIView):
    queryset = HealthDetail.objects.all()
    serializer_class = HealthDetailSerializer
    permission_classes = [IsAdminOrTrainerUser]

class HealthDetailCreateView(generics.CreateAPIView):
    queryset = HealthDetail.objects.all()
    serializer_class = HealthDetailSerializer
    permission_classes = [IsAdminOrTrainerUser]

class HealthDetailUpdateView(generics.UpdateAPIView):
    queryset = HealthDetail.objects.all()
    serializer_class = HealthDetailSerializer
    permission_classes = [IsAdminOrTrainerUser]

class UserHealthDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            health_detail = HealthDetail.objects.get(user=request.user)
            serializer = HealthDetailSerializer(health_detail)
            return Response(serializer.data)
        except HealthDetail.DoesNotExist:
            return Response(
                {"error": "Health details not found for this user"}, 
                status=status.HTTP_404_NOT_FOUND
            )