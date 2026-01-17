from django.db import models
from apps.profiles.models import Student, Teacher


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = "subjects"

    def __str__(self):
        return self.subject_name


class Class(models.Model):
    class_name = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name="classes")

    class Meta:
        db_table = "classes"
        verbose_name_plural = "classes"

    def __str__(self):
        return f"{self.class_name} ({self.academic_year})"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="enrollments", db_column="class_id")

    class Meta:
        db_table = "enrollments"
        unique_together = ["student", "class_obj"]

    def __str__(self):
        return f"{self.student} - {self.class_obj}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="grades")
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    grade_date = models.DateField()

    class Meta:
        db_table = "grades"

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.marks}"
