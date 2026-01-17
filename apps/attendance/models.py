from django.db import models
from apps.profiles.models import Student
from apps.academic.models import Class


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "present"
        ABSENT = "absent"
        LATE = "late"
        EXCUSED = "excused"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendances")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="attendances", db_column="class_id")
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices)

    class Meta:
        db_table = "attendance"

    def __str__(self):
        return f"{self.student} - {self.attendance_date}: {self.status}"
