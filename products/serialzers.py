from rest_framework import serializers
from .models import Product, Wishlist

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "gender", "article_type", "base_colour", "product_display_name", "imageURL"]

class WishlistSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "product", "quantity"]