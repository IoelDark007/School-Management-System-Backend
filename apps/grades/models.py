from django.db import models
from apps.students.models import Student
from apps.academic.models import Subject, Enrollment
from apps.accounts.models import User


class Grade(models.Model):
    """Student grades/marks"""
    
    class GradeType(models.TextChoices):
        ASSIGNMENT = 'assignment', 'Assignment'
        QUIZ = 'quiz', 'Quiz'
        MIDTERM = 'midterm', 'Midterm Exam'
        FINAL = 'final', 'Final Exam'
        PROJECT = 'project', 'Project'
    
    class Term(models.TextChoices):
        TERM_1 = '1', 'Term 1'
        TERM_2 = '2', 'Term 2'
        TERM_3 = '3', 'Term 3'
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='grades')
    
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    grade_type = models.CharField(max_length=20, choices=GradeType.choices)
    exam_date = models.DateField()
    term = models.CharField(max_length=1, choices=Term.choices)
    remarks = models.TextField(blank=True)
    
    entered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='entered_grades'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'grades'
        ordering = ['-exam_date']
        indexes = [
            models.Index(fields=['student', 'subject']),
            models.Index(fields=['enrollment']),
            models.Index(fields=['term']),
        ]
    
    def __str__(self):
        return f"{self.student.full_name} - {self.subject.subject_name}: {self.marks}/{self.max_marks}"
    
    @property
    def percentage(self):
        if self.max_marks > 0:
            return (self.marks / self.max_marks) * 100
        return 0
    
    @property
    def letter_grade(self):
        """Convert percentage to letter grade"""
        pct = self.percentage
        if pct >= 90:
            return 'A+'
        elif pct >= 80:
            return 'A'
        elif pct >= 70:
            return 'B'
        elif pct >= 60:
            return 'C'
        elif pct >= 50:
            return 'D'
        else:
            return 'F'