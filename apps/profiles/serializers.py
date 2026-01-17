from rest_framework import serializers
from apps.profiles.models import Student, Teacher, Parent
from apps.accounts.serializers import UserSerializer

class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Parent
        fields = ["id", "user", "phone_number", "address"]

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    parent = ParentSerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            "id", "user", "parent", "first_name", "last_name",
            "date_of_birth", "status"
        ]

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Teacher
        fields = ["id", "user", "first_name", "last_name", "specialization"]

