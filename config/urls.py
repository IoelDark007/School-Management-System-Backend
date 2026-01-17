# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# Import viewsets
from apps.accounts.views import UserViewSet
from apps.profiles.views import StudentViewSet, TeacherViewSet, ParentViewSet
from apps.academic.views import ClassViewSet, SubjectViewSet, EnrollmentViewSet, GradeViewSet
from apps.attendance.views import AttendanceViewSet
from apps.finance.views import InvoiceViewSet, PaymentViewSet
from apps.hr.views import StaffDetailsViewSet, SalaryViewSet, StaffAttendanceViewSet
from apps.expenditure.views import SchoolExpenditureViewSet
from apps.timetable.views import TimetableViewSet, SyllabusViewSet

# Default router
router = routers.DefaultRouter()

# Accounts 
router.register(r'users', UserViewSet, basename='users')

# Profiles
router.register(r'students', StudentViewSet, basename='students')
router.register(r'teachers', TeacherViewSet, basename='teachers')
router.register(r'parents', ParentViewSet, basename='parents')

# Academic
router.register(r'classes', ClassViewSet, basename='classes')
router.register(r'subjects', SubjectViewSet, basename='subjects')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollments')
router.register(r'grades', GradeViewSet, basename='grades')

# Attendance
router.register(r'attendance', AttendanceViewSet, basename='attendance')

# Finance
router.register(r'invoices', InvoiceViewSet, basename='invoices')
router.register(r'payments', PaymentViewSet, basename='payments')

# HR
router.register(r'staff', StaffDetailsViewSet, basename='staff')
router.register(r'salaries', SalaryViewSet, basename='salaries')
router.register(r'staff-attendance', StaffAttendanceViewSet, basename='staff-attendance')

# Expenditure
router.register(r'expenditure', SchoolExpenditureViewSet, basename='expenditure')

# Timetable
router.register(r'timetables', TimetableViewSet, basename='timetables')
router.register(r'syllabi', SyllabusViewSet, basename='syllabi')


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API routes
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/", include("apps.authentication.urls")),

    # JWT Auth
    #path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    #path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    #path("api/v1/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # API Schema / Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Debug toolbar for development only
from django.conf import settings
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

