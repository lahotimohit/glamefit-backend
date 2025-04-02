from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "gender", "article_type", "base_colour", "product_display_name", "imageURL"]