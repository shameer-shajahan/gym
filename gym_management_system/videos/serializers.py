from rest_framework import serializers
from .models import Video, VideoCategory
from experts.serializers import ExpertProfileSerializer

class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = ['id', 'name', 'description']

class VideoSerializer(serializers.ModelSerializer):
    expert_details = ExpertProfileSerializer(source='expert', read_only=True)
    category_details = VideoCategorySerializer(source='category', read_only=True)
    
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_url', 'thumbnail', 
                  'expert', 'expert_details', 'category', 'category_details', 
                  'duration', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']