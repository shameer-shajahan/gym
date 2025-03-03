from rest_framework import serializers
from .models import HealthDetail
from users.serializers import UserSerializer

class HealthDetailSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    bmi = serializers.FloatField(read_only=True)
    bmi_category = serializers.CharField(read_only=True)
    
    class Meta:
        model = HealthDetail
        fields = ['id', 'user', 'user_details', 'height', 'weight', 'blood_group', 
                  'medical_conditions', 'allergies', 'fitness_goal', 'bmi', 
                  'bmi_category', 'last_updated']
        read_only_fields = ['last_updated']