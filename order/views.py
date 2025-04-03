from rest_framework import viewsets, status, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Cart
from .serializers import CartSerializer


@api_view(["POST", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def manage_cart(request):
    user=request.user
    
    if request.method == "POST":
        product_id = request.data.get("product_id")
        if product_id is None:
            return Response({"error": "please select a product..."}, status=403)
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity+=1
            cart_item.save()
        return Response({"msg": "Product added successfully..."}, status=200)
    
    elif request.method == "DELETE":
        product_id = request.data.get("product_id")
        cart_item = Cart.objects.filter(user=user, product_id=product_id)
        if cart_item:
            cart_item.delete()
            return Response({"msg": "Item removed successfully..."}, status=204)
        return Response({"error": "Item not found in cart..."}, status=404)
    
class CartListView(generics.ListAPIView):
    serializer_class=CartSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)