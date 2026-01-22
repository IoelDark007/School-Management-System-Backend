from rest_framework import serializers
from .models import AcademicYear, Class, Subject, Enrollment, SubjectAssignment
from apps.staff.serializers import StaffSerializer
from apps.students.serializers import StudentSerializer


class AcademicYearSerializer(serializers.ModelSerializer):
    """Serializer for AcademicYear model"""
    
    class Meta:
        model = AcademicYear
        fields = ['id', 'year_name', 'start_date', 'end_date', 'is_current']
        read_only_fields = ['id']


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for Subject model"""
    
    class Meta:
        model = Subject
        fields = ['id', 'subject_name', 'subject_code', 'description', 'grade_level']
        read_only_fields = ['id']


class ClassSerializer(serializers.ModelSerializer):
    """Serializer for Class model"""
    
    class_teacher = StaffSerializer(read_only=True)
    class_teacher_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    academic_year_name = serializers.CharField(source='academic_year.year_name', read_only=True)
    current_enrollment = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Class
        fields = [
            'id', 'class_name', 'grade_level', 'section',
            'academic_year', 'academic_year_name',
            'class_teacher', 'class_teacher_id',
            'capacity', 'current_enrollment', 'room_number'
        ]
        read_only_fields = ['id']


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model"""
    
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    class_obj = ClassSerializer(read_only=True)
    class_id = serializers.IntegerField(write_only=True, source='class_obj')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_id', 'class_obj', 'class_id',
            'enrollment_date', 'status', 'status_display', 'roll_number'
        ]
        read_only_fields = ['id', 'enrollment_date']


class SubjectAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for SubjectAssignment model"""
    
    class_obj = ClassSerializer(read_only=True)
    class_id = serializers.IntegerField(write_only=True, source='class_obj')
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    teacher = StaffSerializer(read_only=True)
    teacher_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = SubjectAssignment
        fields = [
            'id', 'class_obj', 'class_id', 'subject', 'subject_id',
            'teacher', 'teacher_id'
        ]
        read_only_fields = ['id']


class ClassDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Class with enrollments and subjects"""
    
    class_teacher = StaffSerializer(read_only=True)
    academic_year = AcademicYearSerializer(read_only=True)
    enrollments = EnrollmentSerializer(many=True, read_only=True)
    subject_assignments = SubjectAssignmentSerializer(many=True, read_only=True)
    current_enrollment = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Class
        fields = [
            'id', 'class_name', 'grade_level', 'section',
            'academic_year', 'class_teacher', 'capacity',
            'current_enrollment', 'room_number',
            'enrollments', 'subject_assignments'
        ]