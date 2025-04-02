from django.db import models
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