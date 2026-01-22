from django.db import transaction
from django.core.exceptions import ValidationError
from apps.accounts.models import User
from apps.accounts.services import UserService
from .models import Staff, SalaryStructure, SalaryPayment
from datetime import datetime


class StaffService:
    """Service layer for Staff operations"""
    
    @transaction.atomic
    def create_staff_with_user(self, staff_data, user_data=None, created_by=None):
        """
        Atomically create User + Staff profile in a single transaction.
        
        Args:
            staff_data: dict with staff profile information
            user_data: dict with user account information (optional, will be generated if not provided)
            created_by: User object who is creating this staff
        
        Returns:
            Staff object with associated User
        """
        # Validate permissions
        role = staff_data.get('staff_type', 'teacher')
        user_role_map = {
            'teacher': User.Role.TEACHER,
            'headmaster': User.Role.HEADMASTER,
            'bursar': User.Role.BURSAR,
            'admin_staff': User.Role.ADMIN,
            'support_staff': User.Role.TEACHER,  # Support staff get teacher-level access
        }
        
        target_role = user_role_map.get(role, User.Role.TEACHER)
        
        if created_by:
            UserService.validate_role_permissions(created_by, target_role)
        
        # Generate user data if not provided
        if not user_data:
            user_data = {}
        
        # Auto-generate username if not provided
        if 'username' not in user_data:
            user_data['username'] = UserService.generate_username(
                staff_data['first_name'],
                staff_data['last_name'],
                role
            )
        
        # Auto-generate email if not provided
        if 'email' not in user_data:
            user_data['email'] = f"{user_data['username']}@school.com"
        
        # Validate email uniqueness
        UserService.validate_email_unique(user_data['email'])
        
        # Generate password if not provided
        if 'password' not in user_data:
            user_data['password'] = UserService.generate_password()
            generated_password = user_data['password']
        else:
            generated_password = None
        
        # Create User
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            role=target_role,
            created_by=created_by
        )
        
        # Create Staff profile
        staff = Staff.objects.create(
            user=user,
            first_name=staff_data['first_name'],
            last_name=staff_data['last_name'],
            date_of_birth=staff_data.get('date_of_birth'),
            phone_number=staff_data.get('phone_number', ''),
            email=user_data['email'],  # Duplicate for easy access
            address=staff_data.get('address', ''),
            gender=staff_data.get('gender', ''),
            staff_type=role,
            specialization=staff_data.get('specialization', ''),
            employment_date=staff_data.get('employment_date'),
            national_id=staff_data.get('national_id', ''),
            health_info=staff_data.get('health_info', ''),
            photo_url=staff_data.get('photo_url', '')
        )
        
        # Create salary structure if provided
        if 'salary' in staff_data:
            SalaryStructure.objects.create(
                staff=staff,
                base_salary=staff_data['salary'].get('base_salary', 0),
                housing_allowance=staff_data['salary'].get('housing_allowance', 0),
                transport_allowance=staff_data['salary'].get('transport_allowance', 0),
                other_allowances=staff_data['salary'].get('other_allowances', 0),
                effective_from=staff_data['salary'].get('effective_from', datetime.now().date())
            )
        
        return {
            'staff': staff,
            'user': user,
            'generated_password': generated_password,
            'username': user.username
        }
    
    @transaction.atomic
    def update_staff(self, staff_id, staff_data):
        """Update staff information"""
        try:
            staff = Staff.objects.select_related('user').get(id=staff_id)
        except Staff.DoesNotExist:
            raise ValidationError("Staff not found")
        
        # Update Staff fields
        for field, value in staff_data.items():
            if field not in ['user', 'salary'] and hasattr(staff, field):
                setattr(staff, field, value)
        
        # Update email in both User and Staff if provided
        if 'email' in staff_data:
            if staff_data['email'] != staff.user.email:
                UserService.validate_email_unique(staff_data['email'])
                staff.user.email = staff_data['email']
                staff.user.save()
        
        staff.save()
        return staff
    
    @transaction.atomic
    def deactivate_staff(self, staff_id, deactivated_by):
        """Deactivate staff member (disable their user account)"""
        try:
            staff = Staff.objects.select_related('user').get(id=staff_id)
        except Staff.DoesNotExist:
            raise ValidationError("Staff not found")
        
        # Cannot deactivate yourself
        if staff.user == deactivated_by:
            raise ValidationError("You cannot deactivate your own account")
        
        staff.user.is_active = False
        staff.user.save()
        
        return staff
    
    @staticmethod
    def get_staff_by_type(staff_type):
        """Get all staff of a specific type"""
        return Staff.objects.filter(staff_type=staff_type).select_related('user')
    
    @staticmethod
    def get_active_teachers():
        """Get all active teachers"""
        return Staff.objects.filter(
            staff_type='teacher',
            user__is_active=True
        ).select_related('user')


class SalaryService:
    """Service layer for salary operations"""
    
    @transaction.atomic
    def process_monthly_salary(self, staff_id, payment_period, processed_by):
        """
        Process monthly salary for a staff member
        
        Args:
            staff_id: Staff ID
            payment_period: String like "January 2025"
            processed_by: User who is processing the payment
        """
        try:
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            raise ValidationError("Staff not found")
        
        # Check if salary already processed for this period
        if SalaryPayment.objects.filter(staff=staff, payment_period=payment_period).exists():
            raise ValidationError(f"Salary already processed for {payment_period}")
        
        # Get current salary structure
        salary_structure = SalaryStructure.objects.filter(
            staff=staff,
            effective_from__lte=datetime.now().date()
        ).order_by('-effective_from').first()
        
        if not salary_structure:
            raise ValidationError("No salary structure found for this staff")
        
        # Calculate salary components
        base_salary = salary_structure.base_salary
        allowances = (
            salary_structure.housing_allowance +
            salary_structure.transport_allowance +
            salary_structure.other_allowances
        )
        
        # Calculate tax (simplified - 10% of gross)
        gross_salary = base_salary + allowances
        tax = gross_salary * 0.10
        
        # Calculate net salary
        net_salary = gross_salary - tax
        
        # Create salary payment record
        salary_payment = SalaryPayment.objects.create(
            staff=staff,
            payment_period=payment_period,
            base_salary=base_salary,
            allowances=allowances,
            deductions=0,
            tax=tax,
            net_salary=net_salary,
            status=SalaryPayment.PaymentStatus.PENDING,
            processed_by=processed_by
        )
        
        return salary_payment
    
    @transaction.atomic
    def mark_salary_as_paid(self, salary_payment_id, payment_date, payment_method):
        """Mark a salary payment as paid"""
        try:
            salary_payment = SalaryPayment.objects.get(id=salary_payment_id)
        except SalaryPayment.DoesNotExist:
            raise ValidationError("Salary payment not found")
        
        if salary_payment.status == SalaryPayment.PaymentStatus.PAID:
            raise ValidationError("Salary already marked as paid")
        
        salary_payment.status = SalaryPayment.PaymentStatus.PAID
        salary_payment.payment_date = payment_date
        salary_payment.payment_method = payment_method
        salary_payment.save()
        
        return salary_payment