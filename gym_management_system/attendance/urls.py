from django.urls import path
from .views import (
    AttendanceListView, AttendanceDetailView, AttendanceCreateView,
    AttendanceUpdateView, UserAttendanceListView, BatchAttendanceListView,
    MarkAttendanceView
)

urlpatterns = [
    path('', AttendanceListView.as_view(), name='attendance-list'),
    path('<int:pk>/', AttendanceDetailView.as_view(), name='attendance-detail'),
    path('create/', AttendanceCreateView.as_view(), name='attendance-create'),
    path('update/<int:pk>/', AttendanceUpdateView.as_view(), name='attendance-update'),
    path('user/', UserAttendanceListView.as_view(), name='user-attendance-list'),
    path('batch/<int:batch_id>/', BatchAttendanceListView.as_view(), name='batch-attendance-list'),
    path('mark/', MarkAttendanceView.as_view(), name='mark-attendance'),
]