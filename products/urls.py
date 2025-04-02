from django.urls import path
from .views import ProductListView

urlpatterns = [
    path("get-product/", ProductListView.as_view(), name="product-list"),
]
