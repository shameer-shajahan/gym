from rest_framework import serializers
from .models import Attendance
from users.serializers import UserSerializer
from batches.serializers import BatchSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    batch_details = BatchSerializer(source='batch', read_only=True)
    marked_by_details = UserSerializer(source='marked_by', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'user_details', 'batch', 'batch_details', 
                  'date', 'status', 'remarks', 'marked_by', 'marked_by_details', 
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']