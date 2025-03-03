from django.db import models
from users.models import User

class ExpertProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='expert_profile')
    expertise_area = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Experience in years")
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.expertise_area}"