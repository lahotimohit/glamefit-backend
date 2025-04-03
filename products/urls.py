from django.urls import path
from .views import ProductListView, WishlistListView, manage_wishlist

urlpatterns = [
    path("get-product/", ProductListView.as_view(), name="product-list"),
    path("wishlist/", WishlistListView.as_view(), name="wishlist"),
    path("wishlist/manage/", manage_wishlist, name="wishlist-manage"),
]
