from django.db import models
from users.models import User
from trainers.models import TrainerProfile

class Batch(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='batches')
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def current_members_count(self):
        return self.members.count()
    
    @property
    def is_full(self):
        return self.current_members_count >= self.capacity

class BatchMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='batch_memberships')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='members')
    joined_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'batch')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.batch.name}"