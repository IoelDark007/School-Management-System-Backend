from django.db import models
from apps.academic.models import Class, Subject
from apps.profiles.models import Teacher


class Timetable(models.Model):
    class Day(models.TextChoices):
        MONDAY = "Monday"
        TUESDAY = "Tuesday"
        WEDNESDAY = "Wednesday"
        THURSDAY = "Thursday"
        FRIDAY = "Friday"

    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="timetables", db_column="class_id")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="timetables")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="timetables")
    day_of_week = models.CharField(max_length=10, choices=Day.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20)

    class Meta:
        db_table = "timetable"

    def __str__(self):
        return f"{self.class_obj} - {self.subject} ({self.day_of_week})"


class Syllabus(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="syllabi")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="syllabi")
    week_number = models.IntegerField()
    topic_title = models.CharField(max_length=255)
    content_summary = models.TextField(blank=True)
    learning_objectives = models.TextField(blank=True)

    class Meta:
        db_table = "syllabus"
        verbose_name_plural = "syllabi"

    def __str__(self):
        return f"Week {self.week_number}: {self.topic_title}"
