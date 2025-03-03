from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'batch', 'date', 'status', 'marked_by')
    list_filter = ('status', 'date', 'batch')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'batch__name')