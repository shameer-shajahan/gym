from django.db import models
from experts.models import ExpertProfile

class TipCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Tip Categories"

class Tip(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='tip_images/', blank=True, null=True)
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name='tips')
    category = models.ForeignKey(TipCategory, on_delete=models.SET_NULL, null=True, related_name='tips')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title