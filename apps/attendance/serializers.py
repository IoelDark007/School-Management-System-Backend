from rest_framework import serializers
from apps.attendance.models import Attendance
from apps.profiles.serializers import StudentSerializer
from apps.academic.serializers import ClassSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    class_obj = ClassSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "student", "class_obj", "attendance_date", "status"]

