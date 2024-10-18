from django.db import models

PRODUCT_ORDERINGS = (
    ("-created_at", "Hàng mới nhất"),
    ("created_at", "Hàng cũ nhất"),
    ("price", "Giá tăng dần"),
    ("-price", "Giá giảm dần"),
)


class ProductStatus(models.TextChoices):
    ON_SALE = "on_sale", "Đang giảm giá"
    IN_STOCK = "in_stock", "Còn hàng"


class OrderStatus(models.IntegerChoices):
    PENDING = 1, "Đang chờ"
    ONLINE_PAYING = 2, "Chờ thanh toán online"
    PREPARING = 3, "Đang chuẩn bị"
    SHIPPED = 4, "Đã vận chuyển"
    DELIVERED = 5, "Đã nhận"
    CANNCELED = 6, "Đã huỷ đơn"


class PaymentMethods(models.IntegerChoices):
    ONLINE_PAYMENT = 1, "Thanh toán trực tuyến"
    CASH_ON_DELIVERY = 2, "Thanh toán khi nhận hàng"


# class PaymentStatus(models.IntegerChoices):
#     PAID = 1, "Đã thanh toán"
#     UNPAID = 2, "Chưa thanh toán"
#     CANNCELED = 3, "Đã huỷ thanh toán"


# class CouponStatus(models.IntegerChoices):
#     ACTIVE = 1, "Hoạt động"
#     EXPIRED = 2, "Hết hạn"


# class Ratings(models.IntegerChoices):
#     ONE = 1
#     TWO = 2
#     THREE = 3
#     FOR = 4
#     FIVE = 5
