from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'image', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']