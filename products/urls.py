from django.urls import path
from .views import WishlistListView, manage_wishlist, ProductDetailView, ProductRecommendationView

urlpatterns = [
    path("get-product/", ProductDetailView.as_view(), name="product-list"),
    path('product/<uuid:id>/', ProductDetailView.as_view(), name='product-detail'),
    path("wishlist/", WishlistListView.as_view(), name="wishlist"),
    path("wishlist/manage/", manage_wishlist, name="wishlist-manage"),
    path('recommend/', ProductRecommendationView.as_view())
]
