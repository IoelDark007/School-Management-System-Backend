from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role="student", **extra):
        if not email:
            raise ValueError("Email required")
        user = self.model(email=self.normalize_email(email), role=role, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, password, role="admin", **extra)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrator"
        PRINCIPAL = "principal", "Principal"
        TEACHER = "teacher", "Teacher"
        ACCOUNTANT = "accountant", "Accountant"
        STUDENT = "student"
        PARENT = "parent"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    phone = models.CharField(max_length=20, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Security
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    #REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"

    @property
    def is_locked(self):
        return self.locked_until and timezone.now() < self.locked_until

    def increment_failed_login(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_until = timezone.now() + timezone.timedelta(minutes=30)
        self.save(update_fields=["failed_login_attempts", "locked_until"])

    def reset_failed_login(self):
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=["failed_login_attempts", "locked_until"])
