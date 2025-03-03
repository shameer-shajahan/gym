from django.urls import path
from .views import (
    TrainerListView, TrainerDetailView, TrainerCreateView,
    TrainerUpdateView, TrainerDeleteView, TrainerProfileView
)

urlpatterns = [
    path('', TrainerListView.as_view(), name='trainer-list'),
    path('<int:pk>/', TrainerDetailView.as_view(), name='trainer-detail'),
    path('create/', TrainerCreateView.as_view(), name='trainer-create'),
    path('update/<int:pk>/', TrainerUpdateView.as_view(), name='trainer-update'),
    path('delete/<int:pk>/', TrainerDeleteView.as_view(), name='trainer-delete'),
    path('profile/', TrainerProfileView.as_view(), name='trainer-profile'),
]