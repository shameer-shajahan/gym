from django.urls import path
from .views import (
    HealthDetailListView, HealthDetailDetailView, HealthDetailCreateView,
    HealthDetailUpdateView, UserHealthDetailView
)

urlpatterns = [
    path('', HealthDetailListView.as_view(), name='health-detail-list'),
    path('<int:pk>/', HealthDetailDetailView.as_view(), name='health-detail-detail'),
    path('create/', HealthDetailCreateView.as_view(), name='health-detail-create'),
    path('update/<int:pk>/', HealthDetailUpdateView.as_view(), name='health-detail-update'),
    path('user/', UserHealthDetailView.as_view(), name='user-health-detail'),
]