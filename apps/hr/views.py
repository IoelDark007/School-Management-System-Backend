from rest_framework import viewsets
from apps.hr.models import StaffDetails, Salary, StaffAttendance
from apps.hr.serializers import StaffDetailsSerializer, SalarySerializer, StaffAttendanceSerializer
from rest_framework.permissions import IsAuthenticated

class StaffDetailsViewSet(viewsets.ModelViewSet):
    queryset = StaffDetails.objects.all()
    serializer_class = StaffDetailsSerializer
    permission_classes = [IsAuthenticated]

class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated]

class StaffAttendanceViewSet(viewsets.ModelViewSet):
    queryset = StaffAttendance.objects.all()
    serializer_class = StaffAttendanceSerializer
    permission_classes = [IsAuthenticated]

