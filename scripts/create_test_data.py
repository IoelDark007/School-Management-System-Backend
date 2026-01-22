import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from apps.staff.models import Staff
from apps.academic.models import AcademicYear, Class, Subject
from datetime import date

User = get_user_model()

def create_test_data():
    print("Creating test data...")
    
    # 1. Create admin user
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@school.com',
            'role': 'admin',
            'is_active': True,
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('admin123456')
        admin.save()
        print(f"✓ Created admin user: admin / admin123456")
    else:
        print(f"✓ Admin user already exists")
    
    # 2. Create academic year
    academic_year, created = AcademicYear.objects.get_or_create(
        year_name='2024/2025',
        defaults={
            'start_date': date(2024, 9, 1),
            'end_date': date(2025, 6, 30),
            'is_current': True
        }
    )
    print(f"✓ Created academic year: {academic_year.year_name}")
    
    # 3. Create subjects
    subjects_data = [
        {'subject_name': 'Mathematics', 'subject_code': 'MATH101', 'grade_level': 10},
        {'subject_name': 'English', 'subject_code': 'ENG101', 'grade_level': 10},
        {'subject_name': 'Physics', 'subject_code': 'PHY101', 'grade_level': 10},
        {'subject_name': 'Chemistry', 'subject_code': 'CHEM101', 'grade_level': 10},
    ]
    
    for subject_data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            subject_code=subject_data['subject_code'],
            defaults=subject_data
        )
        if created:
            print(f"✓ Created subject: {subject.subject_name}")
    
    print("\n" + "="*50)
    print("Test data created successfully!")
    print("="*50)
    print("\nLogin credentials:")
    print("Username: admin")
    print("Password: admin123456")
    print("="*50)

if __name__ == '__main__':
    create_test_data()