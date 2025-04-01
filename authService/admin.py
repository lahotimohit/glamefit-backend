from django.contrib import admin
from . import models

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'isVerified', 'created_at', 'updated_at', 'is_active']

class OTPVerification(admin.ModelAdmin):
    list_display = ['id', 'user', 'otp', 'otp_expires_at']

admin.site.register(models.User, UserAdmin)
admin.site.register(models.OTPVerification, OTPVerification)