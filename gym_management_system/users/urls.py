from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, UserLogoutView, 
    UserProfileView, ChangePasswordView, UserListView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('list/', UserListView.as_view(), name='user-list'),
]