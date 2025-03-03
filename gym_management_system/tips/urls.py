from django.urls import path
from .views import (
    TipListView, TipDetailView, TipCreateView, TipUpdateView, TipDeleteView,
    TipCategoryListView, TipCategoryDetailView, TipCategoryCreateView,
    ExpertTipListView
)

urlpatterns = [
    path('', TipListView.as_view(), name='tip-list'),
    path('<int:pk>/', TipDetailView.as_view(), name='tip-detail'),
    path('create/', TipCreateView.as_view(), name='tip-create'),
    path('update/<int:pk>/', TipUpdateView.as_view(), name='tip-update'),
    path('delete/<int:pk>/', TipDeleteView.as_view(), name='tip-delete'),
    path('categories/', TipCategoryListView.as_view(), name='tip-category-list'),
    path('categories/<int:pk>/', TipCategoryDetailView.as_view(), name='tip-category-detail'),
    path('categories/create/', TipCategoryCreateView.as_view(), name='tip-category-create'),
    path('expert/', ExpertTipListView.as_view(), name='expert-tip-list'),
]