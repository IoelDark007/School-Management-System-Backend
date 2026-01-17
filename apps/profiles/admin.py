from django.contrib import admin
from .models import Student, Teacher, Parent

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user', 'parent', 'status')
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name', 'user__username', 'parent__user__username')
    ordering = ('last_name', 'first_name')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user', 'specialization')
    search_fields = ('first_name', 'last_name', 'user__username', 'specialization')
    ordering = ('last_name', 'first_name')


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number')
    ordering = ('user__username',)

