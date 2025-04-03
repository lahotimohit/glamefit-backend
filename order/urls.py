from django.urls import path
from .views import CartListView, manage_cart

urlpatterns = [
    path("cart/", CartListView.as_view(), name="cart"),
    path("cart/manage/", manage_cart, name="cart-manage"),
]
