from django.contrib import admin
from .models import TrainerProfile

@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'specialization')
    list_filter = ('specialization', 'experience')