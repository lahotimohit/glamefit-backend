from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Product, Wishlist
from .serialzers import ProductSerializer, WishlistSerializer
import requests

class InfiniteScrollPagination(LimitOffsetPagination):
    default_limit = 12
    max_limit = 50


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
import uuid

class ProductDetailView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = InfiniteScrollPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["gender", "article_type", "base_colour", "sub_category"]
    ordering_fields = ["product_display_name"]
    lookup_field = "id" 

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        if product_id is not None:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def get_object(self):
        product_id = self.kwargs.get(self.lookup_field)
        try:
            return self.queryset.get(id=product_id)
        except (ValueError, Product.DoesNotExist):
            raise generics.Http404("No product found with this ID")

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


class ProductRecommendationView(APIView):
    def post(self, request):
        try:
            image_url = request.data.get('image_url')
            category = request.data.get('category')
            
            if not image_url or not category:
                return Response(
                    {'error': 'image_url and category are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            recommendation_url = "https://mohit112233-recsys-cross.hf.space/recommend"
            payload = {
                'category': category,
                'file': image_url
            }
            response = requests.post(recommendation_url, data=payload)
            print(response)
            response.raise_for_status()
            
            recommendations = response.json().get('recommendations', [])
            product_ids = [rec['product_id'] for rec in recommendations]
            
            products = Product.objects.filter(
                imageURL__in=[f"https://huggingface.co/datasets/mohit112233/recsys-dataset/resolve/main/images/{pid}.jpg" 
                            for pid in product_ids]
            ).values(
                'id',
                'gender',
                'article_type',
                'base_colour',
                'product_display_name',
                'imageURL'
            )
            response_data = {
                'recommendations': list(products),
            }
            return Response(response_data, status=status.HTTP_200_OK)
            
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': f'Failed to process request: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {'error': f'An error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class WishlistListView(generics.ListAPIView):
    serializer_class=WishlistSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)