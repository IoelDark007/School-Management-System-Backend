from rest_framework import serializers
from .models import Timetable
from apps.academic.serializers import ClassSerializer, SubjectSerializer
from apps.staff.serializers import StaffSerializer


class TimetableSerializer(serializers.ModelSerializer):
    """Serializer for Timetable model"""
    
    class_obj = ClassSerializer(read_only=True)
    class_id = serializers.IntegerField(write_only=True, source='class_obj')
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    teacher = StaffSerializer(read_only=True)
    teacher_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = Timetable
        fields = [
            'id', 'class_obj', 'class_id', 'subject', 'subject_id',
            'teacher', 'teacher_id', 'day_of_week', 'day_of_week_display',
            'start_time', 'end_time', 'room_number'
        ]
        read_only_fields = ['id']
    
    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time")