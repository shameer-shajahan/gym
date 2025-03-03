from django.contrib import admin
from .models import HealthDetail

@admin.register(HealthDetail)
class HealthDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'height', 'weight', 'bmi', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')