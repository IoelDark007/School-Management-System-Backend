from django.contrib import admin
from .models import Invoice, Payment

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'total_amount', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('student__user__username',)
    ordering = ('-due_date',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'amount_paid', 'method', 'transaction_date')
    list_filter = ('method', 'transaction_date')
    search_fields = ('invoice__student__user__username',)
    ordering = ('-transaction_date',)

