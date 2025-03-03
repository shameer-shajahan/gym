from django.db import models
from experts.models import ExpertProfile

class VideoCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Video Categories"

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.URLField(help_text="URL to the video (YouTube, Vimeo, etc.)")
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name='videos')
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True, related_name='videos')
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title