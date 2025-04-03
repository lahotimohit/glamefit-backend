from django.contrib import admin
from . import models

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'isVerified', 'created_at', 'updated_at', 'is_active']

class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'otp', 'otp_expires_at']

class BillingDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'country']

admin.site.register(models.User, UserAdmin)
admin.site.register(models.OTPVerification, OTPVerificationAdmin)
admin.site.register(models.BillingDetails, BillingDetailAdmin)