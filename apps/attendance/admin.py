from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'attendance_date', 'status')
    list_filter = ('attendance_date', 'status', 'class_obj')
    search_fields = ('student__user__username', 'class_obj__class_name')
    ordering = ('-attendance_date',)

