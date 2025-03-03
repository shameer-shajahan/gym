from django.contrib import admin
from .models import Tip, TipCategory

@admin.register(TipCategory)
class TipCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('title', 'expert', 'category', 'is_active')
    list_filter = ('is_active', 'category', 'expert')
    search_fields = ('title', 'content', 'expert__user__email')