from django.db import models
from django.conf import settings
from products.models import Product
from uuid import uuid4

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart")
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email + "-" + self.product.product_display_name
    
class BillingDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='billing_details')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    street_address = models.CharField(max_length=500)
    appartment = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=13)

class Order(models.Model):
    STATUS = [
        ('IN PROGRESS', "In Progress"),
        ('SHIPPED', "Shipped"),
        ('DELIVERED', "Delivered"),
        ('RETURNED', "Returned"),
        ('FAILED', "Failed"),
        ('CANCELLED', "Cancelled")
    ]

    PAYMENT_METHOD = [
        ("UPI", "UPI"),
        ("COD", "Cash On Delivery"),
        ("NET BANKING", "Net Banking")
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order")
    quantity = models.IntegerField()
    billing_detail = models.ForeignKey(BillingDetails, on_delete=models.CASCADE, related_name="order")
    status = models.CharField(choices=STATUS, max_length=20, default="IN PROGRESS")
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=25, default="COD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)