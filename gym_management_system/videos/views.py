from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Video, VideoCategory
from .serializers import VideoSerializer, VideoCategorySerializer
from experts.models import ExpertProfile

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsExpertUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'expert'

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.filter(is_active=True)
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Video.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        expert = self.request.query_params.get('expert')
        
        if category:
            queryset = queryset.filter(category_id=category)
        if expert:
            queryset = queryset.filter(expert_id=expert)
            
        return queryset

class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

class VideoCreateView(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAdminUser | IsExpertUser]
    
    def perform_create(self, serializer):
        if self.request.user.role == 'expert':
            try:
                expert_profile = ExpertProfile.objects.get(user=self.request.user)
                serializer.save(expert=expert_profile)
            except ExpertProfile.DoesNotExist:
                raise serializers.ValidationError("Expert profile not found")
        else:
            serializer.save()

class VideoUpdateView(generics.UpdateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAdminUser | IsExpertUser]
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'expert':
            try:
                expert_profile = ExpertProfile.objects.get(user=request.user)
                return obj.expert == expert_profile
            except ExpertProfile.DoesNotExist:
                return False
        return False

class VideoDeleteView(generics.DestroyAPIView):
    queryset = Video.objects.all()
    permission_classes = [IsAdminUser | IsExpertUser]
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'expert':
            try:
                expert_profile = ExpertProfile.objects.get(user=request.user)
                return obj.expert == expert_profile
            except ExpertProfile.DoesNotExist:
                return False
        return False

class VideoCategoryListView(generics.ListAPIView):
    queryset = VideoCategory.objects.all()
    serializer_class = VideoCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class VideoCategoryDetailView(generics.RetrieveAPIView):
    queryset = VideoCategory.objects.all()
    serializer_class = VideoCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class VideoCategoryCreateView(generics.CreateAPIView):
    queryset = VideoCategory.objects.all()
    serializer_class = VideoCategorySerializer
    permission_classes = [IsAdminUser]

class ExpertVideoListView(APIView):
    permission_classes = [IsExpertUser]
    
    def get(self, request):
        try:
            expert_profile = ExpertProfile.objects.get(user=request.user)
            videos = Video.objects.filter(expert=expert_profile)
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data)
        except ExpertProfile.DoesNotExist:
            return Response(
                {"error": "Expert profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )