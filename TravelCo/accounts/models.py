from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.mail import send_mail

import random
from django.utils import timezone

from .manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=12, unique=True, blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    # Define the field to use as the unique identifier for authentication
    USERNAME_FIELD = "email"  # Or "phone"
    REQUIRED_FIELDS = []

    # Constants for verification code
    VERIFICATION_CODE_EXPIRATION_TIME = 300  # 5 minutes (in seconds)
    MAX_VERIFICATION_ATTEMPTS = 3
    VERIFICATION_ATTEMPT_WINDOW = 3600  # 1 hour (in seconds)

    # Fields for tracking verification attempts
    verification_code_timestamp = models.DateTimeField(null=True, blank=True)
    verification_attempts = models.PositiveIntegerField(default=0)
    last_verification_attempt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email or self.phone

    def generate_verification_code(self):
        """Generate a random 6-digit verification code."""
        code = random.randint(100_000, 999_999)
        self.verification_code = code
        self.verification_code_timestamp = timezone.now()
        self.save()

    def verify_verification_code(self, code):
        """Verify the provided verification code."""
        if (
            self.verification_code == code
            and self.verification_code_timestamp
            and timezone.now() - self.verification_code_timestamp
            <= timezone.timedelta(seconds=self.VERIFICATION_CODE_EXPIRATION_TIME)
        ):
            self.verification_attempts = 0  # Reset attempts on successful verification
            self.save()
            return True
        return False

    def record_verification_attempt(self):
        """Record a verification attempt."""
        if (
            not self.last_verification_attempt
            or timezone.now() - self.last_verification_attempt
            >= timezone.timedelta(seconds=self.VERIFICATION_ATTEMPT_WINDOW)
        ):
            self.verification_attempts = 1
        else:
            self.verification_attempts += 1
        self.last_verification_attempt = timezone.now()
        self.save()

    def is_verification_attempts_exceeded(self):
        """Check if verification attempts exceeded."""
        return self.verification_attempts >= self.MAX_VERIFICATION_ATTEMPTS

    def send_verification_code(self):
        """Send the verification code via email."""
        code = self.generate_verification_code()

        subject = "Verification Code"
        message = f"Your verification code is: {code}"
        from_email = "your_email@gmail.com"  # Update with your email
        to_email = self.email

        send_mail(subject, message, from_email, [to_email])


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile',
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=250, blank=True)

    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """Return the short name of the user."""
        return self.first_name
