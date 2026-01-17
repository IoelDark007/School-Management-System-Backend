from django.contrib import admin
from .models import Subject, Class, Enrollment, Grade

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'subject_code')
    search_fields = ('subject_name', 'subject_code')


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'academic_year', 'teacher')
    list_filter = ('academic_year',)
    search_fields = ('class_name', 'teacher__user__username')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj')
    list_filter = ('class_obj',)
    search_fields = ('student__user__username',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks', 'grade_date')
    list_filter = ('grade_date', 'subject')
    search_fields = ('student__user__username', 'subject__subject_name')

