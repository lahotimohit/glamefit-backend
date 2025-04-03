from rest_framework import viewsets, status, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Cart, Order
from products.views import InfiniteScrollPagination
from .serializers import CartSerializer, OrderSerializer, OrderUpdateSerailizer


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
    
@api_view(["POST", "PUT"])
@permission_classes([permissions.IsAuthenticated])
def manage_order(request):
    try:
        user=request.user
        if request.method == "POST":
            product_id = request.data.get("product_id")
            quantity=request.data.get("quantity")
            payment_method=request.data.get("payment_method")
            print(product_id,quantity, payment_method)
            if product_id is None:
                return Response({"error": "please select a product..."}, status=403)
            product = get_object_or_404(Product, id=product_id)
            print(product)
            billing = user.default_billing_address

            if billing is None:
                return Response({"error": "Please select billing address"}, status=404)
            order_item = Order.objects.create(
                user=user, 
                product=product,
                billing_detail=billing,
                quantity=quantity,
                payment_method=payment_method
                )
            order_item.save()
            return Response({"msg": "Order Created Successfully..."}, status=200)
    
        elif request.method == "PUT":
            order_id = request.data.get("order_id")
            order_detail = Order.objects.filter(id=order_id, user=request.user).first()
            if not order_detail:
                return Response({'error': "Order not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = OrderUpdateSerailizer(order_detail, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Order updated successfully."}, status=status.HTTP_200_OK)

            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class OrderListView(generics.ListAPIView):
    serializer_class=OrderSerializer
    permission_classes=[permissions.IsAuthenticated]
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)