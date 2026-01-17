from django.db import models
from apps.accounts.models import User


class StaffDetails(models.Model):
    class Gender(models.TextChoices):
        MALE = "male"
        FEMALE = "female"
        OTHER = "other"

    class StaffType(models.TextChoices):
        TEACHING = "teaching"
        NON_TEACHING = "non-teaching"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_details")
    gender = models.CharField(max_length=10, choices=Gender.choices)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    health_info = models.TextField(blank=True)
    staff_type = models.CharField(max_length=15, choices=StaffType.choices)

    class Meta:
        db_table = "staff_details"
        verbose_name_plural = "staff details"

    def __str__(self):
        return f"{self.user.username}"


class Salary(models.Model):
    class Frequency(models.TextChoices):
        MONTHLY = "monthly"
        WEEKLY = "weekly"

    staff = models.ForeignKey(StaffDetails, on_delete=models.CASCADE, related_name="salaries")
    base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_frequency = models.CharField(max_length=10, choices=Frequency.choices)

    class Meta:
        db_table = "salaries"
        verbose_name_plural = "salaries"

    def __str__(self):
        return f"{self.staff} - {self.base_salary}"


class StaffAttendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "present"
        ABSENT = "absent"
        ON_LEAVE = "on_leave"

    staff = models.ForeignKey(StaffDetails, on_delete=models.CASCADE, related_name="attendances")
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices)

    class Meta:
        db_table = "staff_attendance"

    def __str__(self):
        return f"{self.staff} - {self.status}"
