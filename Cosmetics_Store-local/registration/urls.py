from django.urls import path
from . import views

urlpatterns = [
    path("", views.account, name="account"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("sign_out", views.sign_out, name="sign_out"),
    path("orders", views.orders, name="orders"),
    path("order/detail/<str:id>", views.order_detail, name="order_detail"),
    path("order/delete/<str:id>", views.order_delete, name="order_delete"),
    path("order/cancel/<str:id>", views.order_cancel, name="order_cancel"),
    path("order/delivered/<str:id>", views.order_delivered, name="order_delivered"),
    path(
        "transaction_history",
        views.transaction_history,
        name="transaction_history",
    ),
]
