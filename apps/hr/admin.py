from django.contrib import admin
from .models import StaffDetails, Salary, StaffAttendance

@admin.register(StaffDetails)
class StaffDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_type', 'gender', 'date_of_birth')
    list_filter = ('staff_type', 'gender')
    search_fields = ('user__username', 'user__email')
    ordering = ('user__username',)


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('staff', 'base_salary', 'allowances', 'deductions', 'payment_frequency')
    list_filter = ('payment_frequency',)
    search_fields = ('staff__user__username',)
    ordering = ('-base_salary',)


@admin.register(StaffAttendance)
class StaffAttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'status', 'check_in', 'check_out')
    list_filter = ('status',)
    search_fields = ('staff__user__username',)
    ordering = ('-check_in',)

