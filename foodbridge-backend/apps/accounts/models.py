import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager

ROLE_CHOICES = (
    ('donor', 'Donor'),
    ('ngo', 'NGO'),
    ('volunteer', 'Volunteer'),
    ('corporate', 'Corporate CSR Manager'),
    ('admin', 'Admin (Platform Ops)'),
    ('superadmin', 'Super Admin'),
)

class UserManager(BaseUserManager):
    def create_user(self, phone_number=None, email=None, password=None, username=None, **extra_fields):
        username = username or phone_number
        if not username and not phone_number:
            raise ValueError('Either phone_number or username must be set')
        if not phone_number:
            phone_number = username
        if email:
            email = self.normalize_email(email)
        extra_fields.setdefault('username', username)
        extra_fields.setdefault('phone_number', phone_number)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superadmin')
        return self.create_user(phone_number=phone_number, password=password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='donor')
    full_name = models.CharField(max_length=150)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # Overall verified status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name', 'role']

    def __str__(self):
        return f"{self.full_name} ({self.role}) - {self.phone_number}"

class OTPCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, db_index=True)
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def is_valid(self):
        return not self.is_used and self.attempts < 3 and timezone.now() < self.expires_at

    def __str__(self):
        return f"OTP for {self.phone_number}: {self.code} [Valid: {self.is_valid()}]"

class PasswordResetToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True, db_index=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        return f"Password reset token for {self.user.email or self.user.phone_number}"

class EmailVerificationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification_tokens')
    token = models.CharField(max_length=100, unique=True, db_index=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        return f"Email verification token for {self.user.email}"
