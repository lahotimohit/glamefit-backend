from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from .models import Product
from .serialzers import ProductSerializer

# Pagination class for Infinite Scrolling
class InfiniteScrollPagination(LimitOffsetPagination):
    default_limit = 12  # Number of images per request
    max_limit = 50  # Optional: Prevent fetching too many at once

# Product List API with filtering and infinite scrolling pagination
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = InfiniteScrollPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["gender", "article_type","base_colour","sub_category"]
    ordering_fields = ["product_display_name"]
