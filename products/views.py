from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Product, Wishlist
from .serialzers import ProductSerializer, WishlistSerializer

class InfiniteScrollPagination(LimitOffsetPagination):
    default_limit = 12
    max_limit = 50


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = InfiniteScrollPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["gender", "article_type","base_colour","sub_category"]
    ordering_fields = ["product_display_name"]

@api_view(["POST", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def manage_wishlist(request):
    user=request.user
    
    if request.method == "POST":
        product_id = request.data.get("product_id")
        print(product_id)
        if product_id is None:
            return Response({"error": "please select a product..."}, status=403)
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)
        if not created:
            return Response({"error": "Product is already in wishlist"}, status=400)
        return Response({"msg": "Product added successfully..."}, status=200)
    
    elif request.method == "DELETE":
        product_id = request.data.get("product_id")
        wishlist_item = Wishlist.objects.filter(user=user, product_id=product_id)
        if wishlist_item:
            wishlist_item.delete()
            return Response({"msg": "Item removed successfully..."}, status=200)
        return Response({"error": "Item not found in wishlist..."}, status=404)
    
class WishlistListView(generics.ListAPIView):
    serializer_class=WishlistSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)