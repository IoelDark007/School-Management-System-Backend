from rest_framework import serializers
from apps.academic.models import Class, Subject, Enrollment, Grade
from apps.profiles.serializers import StudentSerializer, TeacherSerializer

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "subject_name", "subject_code"]

class ClassSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = Class
        fields = ["id", "class_name", "academic_year", "teacher"]

class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    class_obj = ClassSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "student", "class_obj"]

class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = ["id", "student", "subject", "marks", "grade_date"]

