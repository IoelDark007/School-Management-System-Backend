from django.db import models
from apps.academic.models import Class, Subject
from apps.staff.models import Staff


class Timetable(models.Model):
    """Weekly timetable for classes"""
    
    class DayOfWeek(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'

    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='timetable_entries')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable_entries')
    teacher = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='timetable_entries'
    )
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'timetable'
        unique_together = ['class_obj', 'day_of_week', 'start_time']
        ordering = ['day_of_week', 'start_time']
        indexes = [
            models.Index(fields=['class_obj', 'day_of_week']),
            models.Index(fields=['teacher']),
        ]
    
    def __str__(self):
        return f"{self.class_obj.class_name} - {self.subject.subject_name} ({self.get_day_of_week_display()} {self.start_time})"