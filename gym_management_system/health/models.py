from django.db import models
from users.models import User

class HealthDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_detail')
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    fitness_goal = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Health details for {self.user.get_full_name()}"
    
    @property
    def bmi(self):
        """Calculate BMI (Body Mass Index)"""
        height_in_meters = float(self.height) / 100
        return round(float(self.weight) / (height_in_meters ** 2), 2)
    
    @property
    def bmi_category(self):
        """Return BMI category"""
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"