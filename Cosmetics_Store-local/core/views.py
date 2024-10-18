from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from itertools import chain
from django.contrib.auth.decorators import login_required
from .models import Product, ShoppingCart, Order, OrderDetail, Blog
from .filters import ProductFilter
from .enums import OrderStatus
from .utils import get_paginator


# Create your views here.
def home(request):
    new_products = Product.objects.filter(quantity__gt=0)[:6]
    new_blogs = Blog.objects.all()[:3]
    delivered_products = Product.objects.filter(
        orderdetail__order__status=OrderStatus.DELIVERED
    ).distinct()[:6]
    most_expensive_products = Product.objects.filter(quantity__gt=0).order_by("-price")
    best_seller_products = list(delivered_products)
    missing_best_seller_products = 6 - len(best_seller_products)

    if missing_best_seller_products > 0:
        existing_ids = {p.id for p in best_seller_products}
        additional_products = most_expensive_products.exclude(id__in=existing_ids)[
            :missing_best_seller_products
        ]
        best_seller_products.extend(additional_products)

    context = {
        "new_products": new_products,
        "new_blogs": new_blogs,
        "best_seller_products": best_seller_products,
    }

    return render(request, "core/home.html", context)


def products(request):
    filter = ProductFilter(
        request.GET,
        queryset=Product.objects.all(),
        request=request,
    )

    paginator = get_paginator(request, filter.qs)

    context = {
        "filter": filter,
        "paginator": paginator,
    }

    return render(request, "core/products.html", context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("sign_in")

        post_data = request.POST.copy()
        quantity = post_data.get("q", None)
        is_buy_now = post_data.get("buy-now", "off")
        next_url = post_data.get("next_url")
        cart_item = None

        if quantity:
            p = Product.objects.get(id=id)
            is_exist_product = ShoppingCart.objects.filter(
                user=request.user,
                product=p,
            )
            if is_exist_product.count() > 0:
                cart_item = is_exist_product.first()
                new_quantity = is_exist_product.first().quantity + int(quantity)
                is_exist_product.update(quantity=new_quantity)
            else:
                cart_item = ShoppingCart.objects.create(
                    user=request.user,
                    product=p,
                    quantity=quantity,
                )

            if next_url:
                return redirect(next_url)

            if is_buy_now == "on":
                url = f"{reverse('cart')}?s={cart_item.id}"
                return redirect(url)

            return redirect("product_detail", id)

    context = {"product": product}

    return render(request, "core/product_detail.html", context)


def blogs(request):
    paginator = get_paginator(request, Blog.objects.all(), 6)

    context = {
        "paginator": paginator,
    }
    return render(request, "core/blogs.html", context)


def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    context = {
        "blog": blog,
    }
    return render(request, "core/blog_detail.html", context)


def about_us(request):
    return render(request, "core/about_us.html")


def search(request):
    search_str = request.GET.get("s")
    products = Product.objects.filter(
        Q(name__icontains=search_str) | Q(tags__name__icontains=search_str)
    ).distinct()[:12]
    blogs = Blog.objects.filter(
        Q(title__icontains=search_str) | Q(tags__name__icontains=search_str)
    ).distinct()[:12]
    found_number = products.count() + blogs.count()

    ctx = {
        "search_str": search_str,
        "found_number": found_number,
        "products": products,
        "blogs": blogs,
    }
    return render(request, "core/search.html", ctx)


@login_required
def cart(request):
    cart_items = ShoppingCart.objects.filter(user=request.user)

    total_payment = 0
    selected_ids = request.GET.getlist("s", [])
    if len(selected_ids) > 0:
        for cid in selected_ids:
            try:
                citem = ShoppingCart.objects.get(id=cid)
                total_payment += citem.get_total_price()
            except:
                pass

    if request.method == "POST":
        post_data = request.POST.copy()
        cart_item_ids = post_data.getlist("cart_item_id", [])

        if len(cart_item_ids) > 0:
            selected_ids = cart_item_ids
            new_order = Order.objects.create(user=request.user)

            for cid in cart_item_ids:
                try:
                    citem = ShoppingCart.objects.get(id=cid)
                    OrderDetail.objects.create(
                        order=new_order,
                        product=citem.product,
                        quantity=citem.quantity,
                    )
                except:
                    pass

            return redirect("order_detail", new_order.id)

    context = {
        "cart_items": cart_items,
        "selected_ids": selected_ids,
        "total_payment": total_payment,
    }

    return render(request, "core/cart.html", context)


def cart_update(request, id):
    cart_item = get_object_or_404(ShoppingCart, id=id, user=request.user)

    if request.method == "POST":
        post_data = request.POST.copy()
        quantity = post_data.get("q", None)
        if quantity:
            cart_item.quantity = quantity
            cart_item.save()

    return redirect("cart")


def cart_delete(request, id):
    cart_item = get_object_or_404(ShoppingCart, id=id, user=request.user)
    cart_item.delete()

    return redirect("cart")


def cart_delete_multiple(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        cart_item_ids = post_data.getlist("cart_item_id", [])

        if len(cart_item_ids) > 0:
            for cid in cart_item_ids:
                try:
                    citem = ShoppingCart.objects.get(id=cid, user=request.user)
                    citem.delete()
                except:
                    pass

    return redirect("cart")


def payment_create(request):

    return render(request, "core/payment_create.html")
