from rest_framework import serializers
from .models import Payment, PaymentAlert
from users.serializers import UserSerializer

class PaymentSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_details', 'amount', 'payment_date', 'payment_method', 
                  'transaction_id', 'status', 'description']
        read_only_fields = ['payment_date']

class PaymentAlertSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = PaymentAlert
        fields = ['id', 'user', 'user_details', 'amount', 'due_date', 'description', 'is_paid', 'created_at']
        read_only_fields = ['created_at']