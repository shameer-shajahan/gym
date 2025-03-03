from django.urls import path
from .views import (
    ExpertListView, ExpertDetailView, ExpertCreateView,
    ExpertUpdateView, ExpertDeleteView, ExpertProfileView
)

urlpatterns = [
    path('', ExpertListView.as_view(), name='expert-list'),
    path('<int:pk>/', ExpertDetailView.as_view(), name='expert-detail'),
    path('create/', ExpertCreateView.as_view(), name='expert-create'),
    path('update/<int:pk>/', ExpertUpdateView.as_view(), name='expert-update'),
    path('delete/<int:pk>/', ExpertDeleteView.as_view(), name='expert-delete'),
    path('profile/', ExpertProfileView.as_view(), name='expert-profile'),
]