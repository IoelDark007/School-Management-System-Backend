from django.contrib import admin
from .models import SchoolExpenditure

@admin.register(SchoolExpenditure)
class SchoolExpenditureAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'category', 'amount', 'transaction_date', 'paid_to')
    list_filter = ('category', 'transaction_date')
    search_fields = ('item_name', 'paid_to')
    ordering = ('-transaction_date',)

