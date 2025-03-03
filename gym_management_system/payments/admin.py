from django.contrib import admin
from .models import Payment, PaymentAlert

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_date', 'payment_method', 'status')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'transaction_id')

@admin.register(PaymentAlert)
class PaymentAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'due_date', 'is_paid')
    list_filter = ('is_paid', 'due_date')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')