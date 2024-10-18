from django.db import models
from django.db.models import Sum, F
from django.utils import timezone
from .enums import OrderStatus, PaymentMethods
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Danh Mục"
        verbose_name = "Danh Mục"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Thương Hiệu"
        verbose_name = "Thương Hiệu"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Tên tags")

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Danh mục",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Thương hiệu",
    )

    name = models.CharField(max_length=150, verbose_name="Tên sản phẩm")
    price = models.FloatField(default=0, verbose_name="Giá")
    old_price = models.FloatField(default=0, verbose_name="Giá cũ")
    quantity = models.IntegerField(default=0, verbose_name="Số lượng")
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(
        upload_to="images/products/",
        default="default/noimage.jpg",
        verbose_name="Ảnh",
    )
    description = CKEditor5Field("Mô tả", config_name="default")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Sản Phẩm"
        verbose_name = "Sản Phẩm"

    def get_discount_percentage(self):
        if self.old_price <= 0:
            return 0
        if self.price >= self.old_price:
            return 0

        discount_percentage = ((self.old_price - self.price) / self.old_price) * 100
        return round(discount_percentage)

    def get_new_state(self):
        today = timezone.now()
        is_new = (
            self.created_at.month == today.month and self.created_at.year == today.year
        )
        return is_new

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    tags = models.ManyToManyField(Tag, blank=True)
    thumbnail = models.ImageField(
        upload_to="images/blogs/",
        default="default/noimage.jpg",
    )
    content = CKEditor5Field("Nội dung", config_name="default")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Tin Tức"
        verbose_name = "Tin Tức"

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Người dùng",
    )

    address = models.CharField(max_length=100, verbose_name="Địa chỉ")
    message = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="Lời nhắn",
    )
    total_payment = models.FloatField(default=0)
    payment_method = models.IntegerField(choices=PaymentMethods.choices, null=True)
    status = models.IntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name="Trạng thái",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Đơn Hàng"
        verbose_name = "Đơn Hàng"

    def get_total_price(self):
        total = OrderDetail.objects.filter(order=self).aggregate(
            total_price=Sum(F("quantity") * F("product__price"))
        )["total_price"]
        return total or 0

    def __str__(self):
        return f"Đơn của {self.user}"


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Đơn hàng",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Sản phẩm",
    )

    quantity = models.IntegerField(default=0, verbose_name="Số lượng")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Chi Tiết Đơn Hàng"
        verbose_name = "Chi Tiết Đơn Hàng"

    def get_total_price(self):
        total = self.product.price * self.quantity
        return total or 0

    def __str__(self):
        if self.order:
            return f"Chi tiết đơn ({self.order.id}) của {self.order.user}"
        else:
            return "-"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Người dùng",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Sản phẩm",
    )

    quantity = models.IntegerField(verbose_name="Số lượng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Giỏ Hàng"
        verbose_name = "Giỏ Hàng"

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = self.quantity * self.product.price
        return total or 0


# class Payment(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

#     transaction_id = models.CharField(max_length=150, default="")
#     payment_method = models.IntegerField(choices=PaymentMethods.choices)
#     payment_status = models.IntegerField(
#         choices=PaymentStatus.choices,
#         default=PaymentStatus.UNPAID,
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Chi tiết thanh toán đơn ({self.order.id})"


# class Coupon(models.Model):
#     code = models.CharField(max_length=50, unique=True)
#     discount_percentage = models.FloatField(default=0)
#     valid_from = models.DateField()
#     valid_until = models.DateField()
#     status = models.IntegerField(
#         choices=CouponStatus.choices,
#         default=CouponStatus.ACTIVE,
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

#     rating = models.IntegerField(choices=Ratings.choices)
#     comment = models.TextField(max_length=500, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user.username
