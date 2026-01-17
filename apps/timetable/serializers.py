from rest_framework import serializers
from apps.timetable.models import Timetable, Syllabus
from apps.academic.serializers import ClassSerializer, SubjectSerializer
from apps.profiles.serializers import TeacherSerializer

class TimetableSerializer(serializers.ModelSerializer):
    class_obj = ClassSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = Timetable
        fields = ["id", "class_obj", "subject", "teacher", "day_of_week", "start_time", "end_time", "room_number"]

class SyllabusSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = Syllabus
        fields = ["id", "subject", "teacher", "week_number", "topic_title", "content_summary", "learning_objectives"]

