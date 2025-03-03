from django.contrib import admin
from .models import Video, VideoCategory

@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'expert', 'category', 'duration', 'is_active')
    list_filter = ('is_active', 'category', 'expert')
    search_fields = ('title', 'description', 'expert__user__email')