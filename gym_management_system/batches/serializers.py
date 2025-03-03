from rest_framework import serializers
from .models import Batch, BatchMember
from users.serializers import UserSerializer
from trainers.serializers import TrainerProfileSerializer

class BatchSerializer(serializers.ModelSerializer):
    trainer_details = TrainerProfileSerializer(source='trainer', read_only=True)
    current_members_count = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Batch
        fields = ['id', 'name', 'description', 'start_time', 'end_time', 'trainer', 
                  'trainer_details', 'capacity', 'is_active', 'current_members_count', 
                  'is_full', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class BatchMemberSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    batch_details = BatchSerializer(source='batch', read_only=True)
    
    class Meta:
        model = BatchMember
        fields = ['id', 'user', 'user_details', 'batch', 'batch_details', 'joined_date']
        read_only_fields = ['joined_date']