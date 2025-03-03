from django.contrib import admin
from .models import Batch, BatchMember

class BatchMemberInline(admin.TabularInline):
    model = BatchMember
    extra = 1

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'trainer', 'capacity', 'is_active')
    list_filter = ('is_active', 'start_time')
    search_fields = ('name', 'description')
    inlines = [BatchMemberInline]

@admin.register(BatchMember)
class BatchMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'batch', 'joined_date')
    list_filter = ('batch', 'joined_date')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'batch__name')