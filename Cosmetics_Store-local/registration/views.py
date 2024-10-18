from django.shortcuts import render, resolve_url, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignInForm, SignUpForm, UpdateUserInfoForm
from core.models import Order, OrderDetail
from core.forms import OrderPaymentPrepareForm
from core.enums import OrderStatus, PaymentMethods


# Create your views here.
@login_required
def account(request):
    form = UpdateUserInfoForm(instance=request.user)

    if request.method == "POST":
        post_data = request.POST.copy()
        is_change_password = post_data.get("change_password", "off")

        if is_change_password == "on":
            change_password_form = PasswordChangeForm(request.user, request.POST)
            if change_password_form.is_valid():
                user = change_password_form.save()
                update_session_auth_hash(request, user)
                return redirect("account")
            else:
                ctx = {
                    "form": form,
                    "change_password_form": change_password_form,
                }
                return render(request, "registration/user_info.html", ctx)

        else:
            form = UpdateUserInfoForm(
                request.POST,
                request.FILES,
                instance=request.user,
            )
            if form.is_valid():
                form.save()

    ctx = {
        "form": form,
    }
    return render(request, "registration/user_info.html", ctx)


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).exclude(status=OrderStatus.PENDING)

    ctx = {
        "orders": orders,
    }
    return render(request, "registration/orders.html", ctx)


def order_detail(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    order_items = OrderDetail.objects.filter(order=order)
    form = OrderPaymentPrepareForm(instance=order)

    shipping_fee = 15000
    total_payment = shipping_fee + order.get_total_price()

    if request.method == "POST":
        post_data = request.POST.copy()
        payment_method = post_data.get("payment_method")
        form = OrderPaymentPrepareForm(post_data, instance=order)

        if form.is_valid():
            order_update = form.save(commit=False)
            if order_update.status == OrderStatus.PENDING:
                if payment_method == str(PaymentMethods.ONLINE_PAYMENT):
                    order_update.status = OrderStatus.ONLINE_PAYING
                else:
                    order_update.status = OrderStatus.PREPARING
                    order_update.save()
                    return redirect("orders")
                order_update.save()
            elif order_update.status == OrderStatus.ONLINE_PAYING:
                order_update.save()

            return redirect("payment_create")

    context = {
        "order": order,
        "order_items": order_items,
        "form": form,
        "shipping_fee": shipping_fee,
        "total_payment": total_payment,
    }

    return render(request, "registration/order_detail.html", context)


def order_delete(request, id):
    order = get_object_or_404(Order, user=request.user, id=id)
    order.delete()

    return redirect("orders")


def order_cancel(request, id):
    order = get_object_or_404(Order, user=request.user, id=id)
    order.status = OrderStatus.CANNCELED
    order.save()

    return redirect("orders")


def order_delivered(request, id):
    order = get_object_or_404(Order, user=request.user, id=id)
    order.status = OrderStatus.DELIVERED
    order.save()

    return redirect("orders")


@login_required
def transaction_history(request):
    return render(request, "registration/transaction_history.html")


def sign_in(request):
    form = SignInForm()
    next_url = request.GET.get("next")

    if request.method == "POST":
        form = SignInForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                redirect_url = next_url or resolve_url("home")
                return redirect(redirect_url)

    ctx = {
        "form": form,
    }

    return render(request, "registration/index.html", ctx)


def sign_up(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sign_in")

    ctx = {
        "form": form,
    }

    return render(request, "registration/index.html", ctx)


def sign_out(request):
    logout(request)
    return redirect("sign_in")
