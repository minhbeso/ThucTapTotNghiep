from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search", views.search, name="search"),
    path("products", views.products, name="products"),
    path("product/<str:id>", views.product_detail, name="product_detail"),
    path("blogs", views.blogs, name="blogs"),
    path("blog/detail/<str:id>", views.blog_detail, name="blog_detail"),
    path("about_us", views.about_us, name="about_us"),
    path("cart", views.cart, name="cart"),
    path("cart/update/<str:id>", views.cart_update, name="cart_update"),
    path("cart/delete/<str:id>", views.cart_delete, name="cart_delete"),
    path(
        "cart/delete_multiple",
        views.cart_delete_multiple,
        name="cart_delete_multiple",
    ),
    path("payment/create", views.payment_create, name="payment_create"),
]
