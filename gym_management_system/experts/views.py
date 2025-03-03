from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ExpertProfile
from .serializers import ExpertProfileSerializer, ExpertCreateSerializer

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsExpertUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'expert'

class ExpertListView(generics.ListAPIView):
    queryset = ExpertProfile.objects.all()
    serializer_class = ExpertProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpertDetailView(generics.RetrieveAPIView):
    queryset = ExpertProfile.objects.all()
    serializer_class = ExpertProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpertCreateView(generics.CreateAPIView):
    serializer_class = ExpertCreateSerializer
    permission_classes = [IsAdminUser]

class ExpertUpdateView(generics.UpdateAPIView):
    queryset = ExpertProfile.objects.all()
    serializer_class = ExpertProfileSerializer
    permission_classes = [IsAdminUser | IsExpertUser]
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.user == request.user

class ExpertDeleteView(generics.DestroyAPIView):
    queryset = ExpertProfile.objects.all()
    permission_classes = [IsAdminUser]
    
    def perform_destroy(self, instance):
        user = instance.user
        instance.delete()
        user.delete()

class ExpertProfileView(APIView):
    permission_classes = [IsExpertUser]
    
    def get(self, request):
        try:
            expert_profile = ExpertProfile.objects.get(user=request.user)
            serializer = ExpertProfileSerializer(expert_profile)
            return Response(serializer.data)
        except ExpertProfile.DoesNotExist:
            return Response(
                {"error": "Expert profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )