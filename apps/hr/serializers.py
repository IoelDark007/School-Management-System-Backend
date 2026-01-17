from rest_framework import serializers
from apps.hr.models import StaffDetails, Salary, StaffAttendance
from apps.accounts.serializers import UserSerializer

class StaffDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StaffDetails
        fields = ["id", "user", "gender", "date_of_birth", "address", "health_info", "staff_type"]

class SalarySerializer(serializers.ModelSerializer):
    staff = StaffDetailsSerializer(read_only=True)

    class Meta:
        model = Salary
        fields = ["id", "staff", "base_salary", "allowances", "deductions", "payment_frequency"]

class StaffAttendanceSerializer(serializers.ModelSerializer):
    staff = StaffDetailsSerializer(read_only=True)

    class Meta:
        model = StaffAttendance
        fields = ["id", "staff", "check_in", "check_out", "status"]

