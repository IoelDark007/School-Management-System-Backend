from django.contrib import admin
from .models import FeeStructure, Invoice, InvoiceItem, Payment, Expenditure


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'amount', 'academic_year', 'class_obj', 'frequency', 'term', 'is_mandatory')
    list_filter = ('academic_year', 'frequency', 'term', 'is_mandatory')
    search_fields = ('category_name',)
    ordering = ('academic_year', 'category_name')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'student', 'academic_year', 'term', 'total_amount', 'amount_paid', 'balance', 'status', 'due_date')
    list_filter = ('status', 'academic_year', 'term', 'due_date')
    search_fields = ('invoice_number', 'student__first_name', 'student__last_name', 'student__admission_number')
    ordering = ('-created_at',)
    readonly_fields = ('invoice_number', 'balance')


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'description', 'amount')
    list_filter = ('invoice',)
    search_fields = ('description', 'invoice__invoice_number')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_number', 'invoice', 'amount_paid', 'payment_method', 'payment_date', 'received_by')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('payment_number', 'invoice__invoice_number', 'transaction_reference')
    ordering = ('-payment_date',)
    readonly_fields = ('payment_number',)


@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ('expenditure_number', 'item_name', 'category', 'amount', 'vendor_name', 'transaction_date', 'approved_by')
    list_filter = ('category', 'transaction_date')
    search_fields = ('expenditure_number', 'item_name', 'vendor_name')
    ordering = ('-transaction_date',)
    readonly_fields = ('expenditure_number',)