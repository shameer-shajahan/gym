from django.db import models
from users.models import User
from batches.models import Batch

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True, null=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marked_attendances')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'batch', 'date')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.batch.name} - {self.date} - {self.status}"