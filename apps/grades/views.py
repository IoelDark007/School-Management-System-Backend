from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, Avg
from .models import Grade
from .serializers import GradeSerializer, GradeCreateSerializer, StudentGradeReportSerializer
from apps.accounts.permissions import CanManageGrades


class GradeViewSet(viewsets.ModelViewSet):
    """ViewSet for Grade management"""
    
    queryset = Grade.objects.select_related('student', 'subject', 'enrollment', 'entered_by').all()
    permission_classes = [IsAuthenticated, CanManageGrades]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return GradeCreateSerializer
        return GradeSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Teachers can only see grades for their assigned subjects
        if self.request.user.role == 'teacher':
            # Get teacher's subject assignments
            from apps.academic.models import SubjectAssignment
            teacher_subjects = SubjectAssignment.objects.filter(
                teacher__user=self.request.user
            ).values_list('subject_id', flat=True)
            queryset = queryset.filter(subject_id__in=teacher_subjects)
        
        # Filter by student
        student_id = self.request.query_params.get('student_id', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # Filter by subject
        subject_id = self.request.query_params.get('subject_id', None)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        
        # Filter by term
        term = self.request.query_params.get('term', None)
        if term:
            queryset = queryset.filter(term=term)
        
        # Filter by grade type
        grade_type = self.request.query_params.get('grade_type', None)
        if grade_type:
            queryset = queryset.filter(grade_type=grade_type)
        
        # Filter by enrollment (class)
        enrollment_id = self.request.query_params.get('enrollment_id', None)
        if enrollment_id:
            queryset = queryset.filter(enrollment_id=enrollment_id)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(entered_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple grades at once"""
        grades_data = request.data.get('grades', [])
        
        if not grades_data:
            return Response(
                {'error': 'grades array is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_grades = []
        errors = []
        
        for grade_data in grades_data:
            serializer = GradeCreateSerializer(data=grade_data)
            if serializer.is_valid():
                grade = Grade.objects.create(
                    **serializer.validated_data,
                    entered_by=request.user
                )
                created_grades.append(grade)
            else:
                errors.append({
                    'data': grade_data,
                    'errors': serializer.errors
                })
        
        return Response({
            'created': GradeSerializer(created_grades, many=True).data,
            'errors': errors
        }, status=status.HTTP_201_CREATED if created_grades else status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def student_report(self, request):
        """Get grade report for a student"""
        student_id = request.query_params.get('student_id')
        term = request.query_params.get('term')
        
        if not student_id or not term:
            return Response(
                {'error': 'student_id and term are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all grades for student in the term
        grades = Grade.objects.filter(
            student_id=student_id,
            term=term
        ).select_related('subject')
        
        if not grades.exists():
            return Response(
                {'error': 'No grades found for this student and term'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calculate totals
        total_marks = sum(grade.marks for grade in grades)
        total_max_marks = sum(grade.max_marks for grade in grades)
        overall_percentage = (total_marks / total_max_marks * 100) if total_max_marks > 0 else 0
        
        from apps.students.models import Student
        student = Student.objects.get(id=student_id)
        
        report_data = {
            'student': student,
            'term': term,
            'grades': grades,
            'total_marks': total_marks,
            'total_max_marks': total_max_marks,
            'overall_percentage': round(overall_percentage, 2)
        }
        
        serializer = StudentGradeReportSerializer(report_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def class_report(self, request):
        """Get grade report for entire class"""
        class_id = request.query_params.get('class_id')
        subject_id = request.query_params.get('subject_id')
        term = request.query_params.get('term')
        
        if not class_id or not subject_id or not term:
            return Response(
                {'error': 'class_id, subject_id, and term are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all enrollments for the class
        from apps.academic.models import Enrollment
        enrollments = Enrollment.objects.filter(
            class_obj_id=class_id,
            status='active'
        ).values_list('id', flat=True)
        
        # Get grades for all students in this class for the subject and term
        grades = Grade.objects.filter(
            enrollment_id__in=enrollments,
            subject_id=subject_id,
            term=term
        ).select_related('student', 'subject')
        
        # Calculate class statistics
        if grades.exists():
            avg_percentage = sum(grade.percentage for grade in grades) / len(grades)
            highest = max(grades, key=lambda g: g.percentage)
            lowest = min(grades, key=lambda g: g.percentage)
            
            return Response({
                'class_id': class_id,
                'subject_id': subject_id,
                'term': term,
                'total_students': len(grades),
                'average_percentage': round(avg_percentage, 2),
                'highest_score': {
                    'student': highest.student.full_name,
                    'marks': float(highest.marks),
                    'percentage': float(highest.percentage)
                },
                'lowest_score': {
                    'student': lowest.student.full_name,
                    'marks': float(lowest.marks),
                    'percentage': float(lowest.percentage)
                },
                'grades': GradeSerializer(grades, many=True).data
            })
        
        return Response({'error': 'No grades found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def subject_statistics(self, request):
        """Get statistics for a subject across all classes"""
        subject_id = request.query_params.get('subject_id')
        term = request.query_params.get('term')
        
        if not subject_id or not term:
            return Response(
                {'error': 'subject_id and term are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        grades = Grade.objects.filter(subject_id=subject_id, term=term)
        
        if grades.exists():
            total_students = grades.count()
            avg_marks = grades.aggregate(Avg('marks'))['marks__avg']
            
            # Grade distribution
            a_plus = grades.filter(marks__gte=90).count()
            a = grades.filter(marks__gte=80, marks__lt=90).count()
            b = grades.filter(marks__gte=70, marks__lt=80).count()
            c = grades.filter(marks__gte=60, marks__lt=70).count()
            d = grades.filter(marks__gte=50, marks__lt=60).count()
            f = grades.filter(marks__lt=50).count()
            
            return Response({
                'subject_id': subject_id,
                'term': term,
                'total_students': total_students,
                'average_marks': round(float(avg_marks), 2),
                'grade_distribution': {
                    'A+': a_plus,
                    'A': a,
                    'B': b,
                    'C': c,
                    'D': d,
                    'F': f
                }
            })
        
        return Response({'error': 'No grades found'}, status=status.HTTP_404_NOT_FOUND)