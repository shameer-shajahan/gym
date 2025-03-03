from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment, PaymentAlert
from .serializers import PaymentSerializer, PaymentAlertSerializer

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]

class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]

class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]

class PaymentAlertListView(generics.ListAPIView):
    queryset = PaymentAlert.objects.all()
    serializer_class = PaymentAlertSerializer
    permission_classes = [IsAdminUser]

class PaymentAlertDetailView(generics.RetrieveAPIView):
    queryset = PaymentAlert.objects.all()
    serializer_class = PaymentAlertSerializer
    permission_classes = [IsAdminUser]

class PaymentAlertCreateView(generics.CreateAPIView):
    queryset = PaymentAlert.objects.all()
    serializer_class = PaymentAlertSerializer
    permission_classes = [IsAdminUser]

class UserPaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

class UserPaymentAlertListView(generics.ListAPIView):
    serializer_class = PaymentAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PaymentAlert.objects.filter(user=self.request.user)

class MakePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        alert_id = request.data.get('alert_id')
        payment_method = request.data.get('payment_method')
        
        if not alert_id or not payment_method:
            return Response(
                {"error": "Alert ID and payment method are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            alert = PaymentAlert.objects.get(id=alert_id, user=request.user, is_paid=False)
        except PaymentAlert.DoesNotExist:
            return Response(
                {"error": "Payment alert not found or already paid"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create payment
        payment = Payment.objects.create(
            user=request.user,
            amount=alert.amount,
            payment_method=payment_method,
            status='completed',
            description=f"Payment for {alert.description}"
        )
        
        # Mark alert as paid
        alert.is_paid = True
        alert.save()
        
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)