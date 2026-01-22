from rest_framework import serializers
from .models import Grade
from apps.students.serializers import StudentSerializer
from apps.academic.serializers import SubjectSerializer


class GradeSerializer(serializers.ModelSerializer):
    """Serializer for Grade model"""
    
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    enrollment_id = serializers.IntegerField(write_only=True)
    grade_type_display = serializers.CharField(source='get_grade_type_display', read_only=True)
    term_display = serializers.CharField(source='get_term_display', read_only=True)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    letter_grade = serializers.CharField(read_only=True)
    entered_by_username = serializers.CharField(source='entered_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Grade
        fields = [
            'id', 'student', 'student_id', 'subject', 'subject_id',
            'enrollment_id', 'marks', 'max_marks', 'percentage', 'letter_grade',
            'grade_type', 'grade_type_display', 'exam_date',
            'term', 'term_display', 'remarks',
            'entered_by', 'entered_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GradeCreateSerializer(serializers.Serializer):
    """Serializer for creating grades"""
    
    student_id = serializers.IntegerField()
    subject_id = serializers.IntegerField()
    enrollment_id = serializers.IntegerField()
    marks = serializers.DecimalField(max_digits=5, decimal_places=2)
    max_marks = serializers.DecimalField(max_digits=5, decimal_places=2, default=100)
    grade_type = serializers.ChoiceField(choices=Grade.GradeType.choices)
    exam_date = serializers.DateField()
    term = serializers.ChoiceField(choices=Grade.Term.choices)
    remarks = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        if data['marks'] > data['max_marks']:
            raise serializers.ValidationError("Marks cannot exceed max marks")
        return data


class StudentGradeReportSerializer(serializers.Serializer):
    """Serializer for student grade report"""
    
    student = StudentSerializer(read_only=True)
    term = serializers.CharField()
    grades = GradeSerializer(many=True, read_only=True)
    total_marks = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_max_marks = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    overall_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)