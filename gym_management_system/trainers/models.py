from django.db import models
from users.models import User

class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Experience in years")
    bio = models.TextField(blank=True, null=True)
    certification = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"