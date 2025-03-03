from django.urls import path
from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('update/<int:pk>/', EventUpdateView.as_view(), name='event-update'),
    path('delete/<int:pk>/', EventDeleteView.as_view(), name='event-delete'),
]