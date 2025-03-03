from django.urls import path
from .views import (
    VideoListView, VideoDetailView, VideoCreateView, VideoUpdateView, VideoDeleteView,
    VideoCategoryListView, VideoCategoryDetailView, VideoCategoryCreateView,
    ExpertVideoListView
)

urlpatterns = [
    path('', VideoListView.as_view(), name='video-list'),
    path('<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('create/', VideoCreateView.as_view(), name='video-create'),
    path('update/<int:pk>/', VideoUpdateView.as_view(), name='video-update'),
    path('delete/<int:pk>/', VideoDeleteView.as_view(), name='video-delete'),
    path('categories/', VideoCategoryListView.as_view(), name='video-category-list'),
    path('categories/<int:pk>/', VideoCategoryDetailView.as_view(), name='video-category-detail'),
    path('categories/create/', VideoCategoryCreateView.as_view(), name='video-category-create'),
    path('expert/', ExpertVideoListView.as_view(), name='expert-video-list'),
]