from django.db import models
from apps.students.models import Student
from apps.academic.models import Class
from apps.accounts.models import User


class Attendance(models.Model):
    """Daily attendance records for students"""
    
    class AttendanceStatus(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        LATE = 'late', 'Late'
        EXCUSED = 'excused', 'Excused'
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendance_records')
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=AttendanceStatus.choices)
    remarks = models.TextField(blank=True)
    
    marked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='marked_attendance'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'attendance'
        unique_together = ['student', 'attendance_date']
        ordering = ['-attendance_date']
        indexes = [
            models.Index(fields=['attendance_date']),
            models.Index(fields=['class_obj', 'attendance_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.student.full_name} - {self.attendance_date} ({self.get_status_display()})"