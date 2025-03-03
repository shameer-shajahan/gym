from rest_framework import serializers
from .models import ExpertProfile
from users.serializers import UserSerializer

class ExpertProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ExpertProfile
        fields = ['id', 'user', 'expertise_area', 'qualification', 'experience', 'bio']

class ExpertCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = ExpertProfile
        fields = ['email', 'password', 'first_name', 'last_name', 'expertise_area', 'qualification', 'experience', 'bio']
    
    def create(self, validated_data):
        from users.models import User
        
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='expert'
        )
        
        expert_profile = ExpertProfile.objects.create(user=user, **validated_data)
        return expert_profile