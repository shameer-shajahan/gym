from rest_framework import serializers
from .models import Tip, TipCategory
from experts.serializers import ExpertProfileSerializer

class TipCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TipCategory
        fields = ['id', 'name', 'description']

class TipSerializer(serializers.ModelSerializer):
    expert_details = ExpertProfileSerializer(source='expert', read_only=True)
    category_details = TipCategorySerializer(source='category', read_only=True)
    
    class Meta:
        model = Tip
        fields = ['id', 'title', 'content', 'image', 'expert', 'expert_details', 
                  'category', 'category_details', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']