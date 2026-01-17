from django.db import models
from apps.accounts.models import User


class Student(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active"
        GRADUATED = "graduated"
        INACTIVE = "inactive"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    parent = models.ForeignKey("Parent", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        db_table = "students"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "teachers"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="parent_profile")
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        db_table = "parents"

    def __str__(self):
        return f"{self.user.username}"
