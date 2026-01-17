from rest_framework import viewsets
from apps.timetable.models import Timetable, Syllabus
from apps.timetable.serializers import TimetableSerializer, SyllabusSerializer
from rest_framework.permissions import IsAuthenticated

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAuthenticated]

class SyllabusViewSet(viewsets.ModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    permission_classes = [IsAuthenticated]

