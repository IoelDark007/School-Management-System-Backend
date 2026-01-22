from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Student, Parent, StudentParent
from .serializers import (
    StudentSerializer, StudentCreateSerializer, StudentUpdateSerializer,
    ParentSerializer, StudentParentSerializer, StudentDetailSerializer
)
from .services import StudentService, ParentService
from apps.accounts.permissions import CanManageStudents


class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet for Student management"""
    
    queryset = Student.objects.all()
    permission_classes = [IsAuthenticated, CanManageStudents]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return StudentUpdateSerializer
        elif self.action == 'retrieve':
            return StudentDetailSerializer
        return StudentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by gender
        gender = self.request.query_params.get('gender', None)
        if gender:
            queryset = queryset.filter(gender=gender)
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(middle_name__icontains=search) |
                Q(admission_number__icontains=search)
            )
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Register a new student"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Prepare student data
        student_data = {
            'admission_number': serializer.validated_data['admission_number'],
            'first_name': serializer.validated_data['first_name'],
            'last_name': serializer.validated_data['last_name'],
            'middle_name': serializer.validated_data.get('middle_name', ''),
            'date_of_birth': serializer.validated_data['date_of_birth'],
            'gender': serializer.validated_data['gender'],
            'address': serializer.validated_data.get('address', ''),
            'nationality': serializer.validated_data.get('nationality', ''),
            'religion': serializer.validated_data.get('religion', ''),
            'blood_group': serializer.validated_data.get('blood_group', ''),
            'medical_conditions': serializer.validated_data.get('medical_conditions', ''),
            'admission_date': serializer.validated_data.get('admission_date'),
            'photo_url': serializer.validated_data.get('photo_url', ''),
        }
        
        # Parent data
        parent_data_list = serializer.validated_data.get('parents', [])
        
        # Class enrollment
        class_id = serializer.validated_data.get('class_id')
        
        # Register student
        service = StudentService()
        try:
            result = service.register_student(
                student_data=student_data,
                parent_data_list=parent_data_list,
                class_id=class_id,
                created_by=request.user
            )
            
            response_data = StudentDetailSerializer(result['student']).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Update student information"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        service = StudentService()
        try:
            student = service.update_student(instance.id, serializer.validated_data)
            return Response(StudentSerializer(student).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def add_parent(self, request, pk=None):
        """Add a parent to a student"""
        student = self.get_object()
        
        parent_data = request.data
        
        service = StudentService()
        try:
            parent = service.add_parent_to_student(student.id, parent_data)
            return Response(ParentSerializer(parent).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def transfer_class(self, request, pk=None):
        """Transfer student to a new class"""
        student = self.get_object()
        
        new_class_id = request.data.get('class_id')
        if not new_class_id:
            return Response(
                {'error': 'class_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        service = StudentService()
        try:
            enrollment = service.transfer_student(student.id, new_class_id)
            from apps.academic.serializers import EnrollmentSerializer
            return Response(EnrollmentSerializer(enrollment).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def full_details(self, request, pk=None):
        """Get full student details with parents, grades, attendance"""
        student = self.get_object()
        
        service = StudentService()
        try:
            details = service.get_student_with_details(student.id)
            
            from apps.grades.serializers import GradeSerializer
            from apps.attendance.serializers import AttendanceSerializer
            from apps.academic.serializers import EnrollmentSerializer
            
            return Response({
                'student': StudentSerializer(details['student']).data,
                'parents': ParentSerializer(details['parents'], many=True).data,
                'current_enrollment': EnrollmentSerializer(details['current_enrollment']).data if details['current_enrollment'] else None,
                'recent_grades': GradeSerializer(details['grades'][:10], many=True).data,
                'recent_attendance': AttendanceSerializer(details['attendance'][:30], many=True).data,
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ParentViewSet(viewsets.ModelViewSet):
    """ViewSet for Parent management"""
    
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated, CanManageStudents]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone_number__icontains=search) |
                Q(email__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def children(self, request, pk=None):
        """Get all children linked to a parent"""
        parent = self.get_object()
        
        service = ParentService()
        try:
            children = service.get_parent_children(parent.id)
            return Response(StudentSerializer(children, many=True).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentParentViewSet(viewsets.ModelViewSet):
    """ViewSet for StudentParent relationship management"""
    
    queryset = StudentParent.objects.select_related('student', 'parent').all()
    serializer_class = StudentParentSerializer
    permission_classes = [IsAuthenticated, CanManageStudents]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by student
        student_id = self.request.query_params.get('student_id', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # Filter by parent
        parent_id = self.request.query_params.get('parent_id', None)
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        
        return queryset