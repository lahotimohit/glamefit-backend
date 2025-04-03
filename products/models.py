from django.db import models
from authService.models import User 
from uuid import uuid4

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    gender = models.CharField(max_length=10)
    master_category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    article_type = models.CharField(max_length=100)
    base_colour = models.CharField(max_length=50)
    product_display_name = models.CharField(max_length=255)
    imageURL = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.product_display_name


class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " - " + self.product.product_display_name
