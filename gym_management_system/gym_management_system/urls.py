"""
URL configuration for gym_management_system project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/trainers/', include('trainers.urls')),
    path('api/experts/', include('experts.urls')),
    path('api/events/', include('events.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/batches/', include('batches.urls')),
    path('api/health/', include('health.urls')),
    path('api/videos/', include('videos.urls')),
    path('api/tips/', include('tips.urls')),
    path('api/chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)