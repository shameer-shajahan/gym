from django.urls import path
from .views import (
    PaymentListView, PaymentDetailView, PaymentCreateView,
    PaymentAlertListView, PaymentAlertDetailView, PaymentAlertCreateView,
    UserPaymentListView, UserPaymentAlertListView, MakePaymentView
)

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),
    path('<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('create/', PaymentCreateView.as_view(), name='payment-create'),
    path('alerts/', PaymentAlertListView.as_view(), name='payment-alert-list'),
    path('alerts/<int:pk>/', PaymentAlertDetailView.as_view(), name='payment-alert-detail'),
    path('alerts/create/', PaymentAlertCreateView.as_view(), name='payment-alert-create'),
    path('user/', UserPaymentListView.as_view(), name='user-payment-list'),
    path('user/alerts/', UserPaymentAlertListView.as_view(), name='user-payment-alert-list'),
    path('make-payment/', MakePaymentView.as_view(), name='make-payment'),
]