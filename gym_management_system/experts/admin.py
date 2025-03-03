from django.contrib import admin
from .models import ExpertProfile

@admin.register(ExpertProfile)
class ExpertProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise_area', 'qualification')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'expertise_area')
    list_filter = ('expertise_area',)