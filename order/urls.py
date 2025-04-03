from django.urls import path
from .views import CartListView, manage_cart, OrderListView, manage_order

urlpatterns = [
    path("cart/", CartListView.as_view(), name="cart"),
    path("cart/manage/", manage_cart, name="cart-manage"),
    path("order/", OrderListView.as_view(), name="cart"),
    path("order/manage/", manage_order, name="cart-manage"),
]
