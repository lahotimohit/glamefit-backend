from rest_framework.serializers import ModelSerializer
from products.serialzers import ProductSerializer
from authService.serializers import BillingDetailsSerailizer
from . import models

class CartSerializer(ModelSerializer):
    product=ProductSerializer(read_only=True)
    class Meta:
        model = models.Cart
        fields = ["id", "quantity", "product"]

class OrderSerializer(ModelSerializer):
    product=ProductSerializer(read_only=True)
    billing=BillingDetailsSerailizer(source="billing_detail",read_only=True)
    class Meta:
        model = models.Order
        exclude = ["user", "billing_detail"]

class OrderUpdateSerailizer(ModelSerializer):
    class Meta:
        model = models.Order
        fields = ["status"]

        def create(self, validated_data):
            user = self.context.get('user')
            return models.Order.objects.create(user=user, **validated_data)