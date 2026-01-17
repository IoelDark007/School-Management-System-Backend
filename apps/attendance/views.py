from rest_framework import viewsets
from apps.attendance.models import Attendance
from apps.attendance.serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

