from django.urls import path
from .views import (
    BatchListView, BatchDetailView, BatchCreateView, BatchUpdateView, BatchDeleteView,
    BatchMemberListView, BatchMemberCreateView, BatchMemberDeleteView,
    TrainerBatchListView, UserBatchListView
)

urlpatterns = [
    path('', BatchListView.as_view(), name='batch-list'),
    path('<int:pk>/', BatchDetailView.as_view(), name='batch-detail'),
    path('create/', BatchCreateView.as_view(), name='batch-create'),
    path('update/<int:pk>/', BatchUpdateView.as_view(), name='batch-update'),
    path('delete/<int:pk>/', BatchDeleteView.as_view(), name='batch-delete'),
    path('members/', BatchMemberListView.as_view(), name='batch-member-list'),
    path('members/create/', BatchMemberCreateView.as_view(), name='batch-member-create'),
    path('members/delete/<int:pk>/', BatchMemberDeleteView.as_view(), name='batch-member-delete'),
    path('trainer/', TrainerBatchListView.as_view(), name='trainer-batch-list'),
    path('user/', UserBatchListView.as_view(), name='user-batch-list'),
]