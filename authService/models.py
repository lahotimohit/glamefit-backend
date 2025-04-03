import uuid
from django.db import models
from order.models import BillingDetails
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta
from django.contrib.auth.models import AbstractUser

def defaultExpiry():
    return now() + timedelta(minutes=5)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone = models.CharField(max_length=13, unique=True)
    isVerified = models.BooleanField(default=False)
    default_billing_address = models.ForeignKey(BillingDetails, on_delete=models.CASCADE, related_name="billing", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self._state.adding and self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.set_password(self.password)
        super().save(*args, **kwargs)

class OTPVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otp_verification")
    otp = models.CharField(max_length=6)
    otp_expires_at = models.DateTimeField(default=defaultExpiry)

    def is_expired(self):
        return now() > self.otp_expires_at
