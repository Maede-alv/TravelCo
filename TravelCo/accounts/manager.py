from django.contrib.auth.models import BaseUserManager
import re


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone=None,
                    password=None, **extra_fields):
        # Ensure either email or phone number is provided
        if not email and not phone:
            raise ValueError("Either email or phone number must be set")

        # Validate email
        if email:
            email = self.normalize_email(email)
            # Check if email format is valid
            if not re.match(
                r"^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$", email
            ):
                raise ValueError("Invalid email format")

        # Validate phone number
        if phone:
            # Check if phone number format is valid (Iranian phone number)
            if not re.match(r"^\+?98\d{9}$", phone):
                raise ValueError("Invalid phone number format")

        # Create and save the user
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Ensure is_staff and is_superuser are set to True
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Create and save the superuser
        return self.create_user(email, password, **extra_fields)
