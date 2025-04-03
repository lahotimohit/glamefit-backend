from rest_framework.serializers import ModelSerializer
from products.serialzers import ProductSerializer
from . import models

class CartSerializer(ModelSerializer):
    product=ProductSerializer(read_only=True)
    class Meta:
        model = models.Cart
        fields = ["id", "quantity", "product"]