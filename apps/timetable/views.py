from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Timetable
from .serializers import TimetableSerializer
from apps.accounts.permissions import IsAdminOrHeadmaster


class TimetableViewSet(viewsets.ModelViewSet):
    """ViewSet for Timetable management"""
    
    queryset = Timetable.objects.select_related('class_obj', 'subject', 'teacher').all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrHeadmaster()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by class
        class_id = self.request.query_params.get('class_id', None)
        if class_id:
            queryset = queryset.filter(class_obj_id=class_id)
        
        # Filter by teacher
        teacher_id = self.request.query_params.get('teacher_id', None)
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        
        # Filter by day
        day = self.request.query_params.get('day', None)
        if day:
            queryset = queryset.filter(day_of_week=day)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def class_schedule(self, request):
        """Get full weekly schedule for a class"""
        class_id = request.query_params.get('class_id')
        
        if not class_id:
            return Response(
                {'error': 'class_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        timetable_entries = Timetable.objects.filter(
            class_obj_id=class_id
        ).select_related('subject', 'teacher').order_by('day_of_week', 'start_time')
        
        # Group by day
        schedule = {}
        for entry in timetable_entries:
            day = entry.get_day_of_week_display()
            if day not in schedule:
                schedule[day] = []
            
            schedule[day].append(TimetableSerializer(entry).data)
        
        return Response(schedule)
    
    @action(detail=False, methods=['get'])
    def teacher_schedule(self, request):
        """Get full weekly schedule for a teacher"""
        teacher_id = request.query_params.get('teacher_id')
        
        if not teacher_id:
            return Response(
                {'error': 'teacher_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        timetable_entries = Timetable.objects.filter(
            teacher_id=teacher_id
        ).select_related('class_obj', 'subject').order_by('day_of_week', 'start_time')
        
        # Group by day
        schedule = {}
        for entry in timetable_entries:
            day = entry.get_day_of_week_display()
            if day not in schedule:
                schedule[day] = []
            
            schedule[day].append(TimetableSerializer(entry).data)
        
        return Response(schedule)
    
    @action(detail=False, methods=['post'])
    def check_conflicts(self, request):
        """Check for scheduling conflicts"""
        class_id = request.data.get('class_id')
        teacher_id = request.data.get('teacher_id')
        day_of_week = request.data.get('day_of_week')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        exclude_id = request.data.get('exclude_id')  # For updates
        
        conflicts = []
        
        # Check class conflicts
        if class_id:
            class_conflicts = Timetable.objects.filter(
                class_obj_id=class_id,
                day_of_week=day_of_week,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            
            if exclude_id:
                class_conflicts = class_conflicts.exclude(id=exclude_id)
            
            if class_conflicts.exists():
                conflicts.append({
                    'type': 'class',
                    'message': 'Class already has a session at this time',
                    'entries': TimetableSerializer(class_conflicts, many=True).data
                })
        
        # Check teacher conflicts
        if teacher_id:
            teacher_conflicts = Timetable.objects.filter(
                teacher_id=teacher_id,
                day_of_week=day_of_week,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            
            if exclude_id:
                teacher_conflicts = teacher_conflicts.exclude(id=exclude_id)
            
            if teacher_conflicts.exists():
                conflicts.append({
                    'type': 'teacher',
                    'message': 'Teacher already has a session at this time',
                    'entries': TimetableSerializer(teacher_conflicts, many=True).data
                })
        
        return Response({
            'has_conflicts': len(conflicts) > 0,
            'conflicts': conflicts
        })