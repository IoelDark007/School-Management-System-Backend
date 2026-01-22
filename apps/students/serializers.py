from rest_framework import serializers
from typing import List, Dict, Any, Optional
from drf_spectacular.utils import extend_schema_field
from .models import Student, Parent, StudentParent


class ParentSerializer(serializers.ModelSerializer):
    """Serializer for Parent model"""
    
    full_name = serializers.CharField(read_only=True)
    relationship_display = serializers.CharField(source='get_relationship_display', read_only=True)
    
    class Meta:
        model = Parent
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'phone_number', 'email', 'address', 'occupation',
            'workplace', 'national_id', 'relationship', 'relationship_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'admission_number', 'first_name', 'last_name', 'middle_name',
            'full_name', 'date_of_birth', 'age', 'gender', 'gender_display',
            'address', 'nationality', 'religion', 'blood_group', 'medical_conditions',
            'status', 'status_display', 'admission_date', 'photo_url',
            'created_by', 'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Student with parents and enrollment"""
    
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    parents = serializers.SerializerMethodField()
    current_class = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'admission_number', 'first_name', 'last_name', 'middle_name',
            'full_name', 'date_of_birth', 'age', 'gender',
            'address', 'nationality', 'religion', 'blood_group', 'medical_conditions',
            'status', 'admission_date', 'photo_url',
            'parents', 'current_class', 'created_at', 'updated_at'
        ]
    
    @extend_schema_field(serializers.ListSerializer(child=serializers.DictField()))
    def get_parents(self, obj) -> List[Dict[str, Any]]:
        """Get all parents linked to this student"""
        parent_links = obj.parent_links.select_related('parent').all()
        return [{
            'parent': ParentSerializer(link.parent).data,
            'is_primary_contact': link.is_primary_contact,
            'can_pickup': link.can_pickup
        } for link in parent_links]
    
    @extend_schema_field(serializers.DictField())
    def get_current_class(self, obj) -> Optional[Dict[str, Any]]:
        """Get student's current class enrollment"""
        from apps.academic.serializers import EnrollmentSerializer
        enrollment = obj.enrollments.filter(status='active').select_related('class_obj').first()
        if enrollment:
            return EnrollmentSerializer(enrollment).data
        return None


class StudentCreateSerializer(serializers.Serializer):
    """Serializer for creating students"""
    
    # Student fields
    admission_number = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    middle_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
    date_of_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=Student.Gender.choices)
    address = serializers.CharField(required=False, allow_blank=True)
    nationality = serializers.CharField(max_length=50, required=False, allow_blank=True)
    religion = serializers.CharField(max_length=50, required=False, allow_blank=True)
    blood_group = serializers.CharField(max_length=5, required=False, allow_blank=True)
    medical_conditions = serializers.CharField(required=False, allow_blank=True)
    admission_date = serializers.DateField(required=False)
    photo_url = serializers.URLField(required=False, allow_blank=True)
    
    # Class enrollment (optional)
    class_id = serializers.IntegerField(required=False, allow_null=True)
    
    # Parents (optional)
    parents = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        allow_empty=True
    )


class StudentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating student information"""
    
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'middle_name', 'date_of_birth',
            'gender', 'address', 'nationality', 'religion', 'blood_group',
            'medical_conditions', 'status', 'photo_url'
        ]


class StudentParentSerializer(serializers.ModelSerializer):
    """Serializer for StudentParent relationship"""
    
    student = StudentSerializer(read_only=True)
    parent = ParentSerializer(read_only=True)
    
    class Meta:
        model = StudentParent
        fields = ['id', 'student', 'parent', 'is_primary_contact', 'can_pickup']
        read_only_fields = ['id']