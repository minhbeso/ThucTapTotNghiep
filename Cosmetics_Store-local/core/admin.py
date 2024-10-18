from django.contrib import admin
from django.utils.html import format_html
from .utils import format_number_with_commas, format_datetime_vn
from .models import (
    Category,
    Brand,
    Product,
    Order,
    OrderDetail,
    ShoppingCart,
    Blog,
    Tag,
)


# Register your models here.
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "brand",
        "formatted_price",
        "quantity",
        "image_tag",
    )
    list_filter = ("category", "price", "quantity")
    search_fields = ["name"]
    filter_horizontal = ("tags",)

    def formatted_price(self, obj):
        total_price = format_number_with_commas(obj.price)
        return f"{total_price} đ"

    formatted_price.short_description = "Giá"

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height:50px;" />'.format(
                    obj.image.url
                )
            )
        return "-"

    image_tag.short_description = "Ảnh"


class BlogAdmin(admin.ModelAdmin):
    filter_horizontal = ("tags",)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "quantity",
        "formatted_created_at",
    )
    list_filter = ["user", "product", "created_at"]
    search_fields = ("user__username", "product")
    ordering = ("-created_at",)

    def formatted_created_at(self, obj):
        created_at = obj.created_at
        return format_datetime_vn(created_at)

    formatted_created_at.short_description = "Ngày tạo"


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "status",
        "formatted_total_price",
        "formatted_created_at",
        "id",
    )
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "status")
    ordering = ("-created_at",)

    def formatted_total_price(self, obj):
        total_price = format_number_with_commas(obj.get_total_price())
        return f"{total_price} đ"

    formatted_total_price.short_description = "Tổng tiền"

    def formatted_created_at(self, obj):
        created_at = obj.created_at
        return format_datetime_vn(created_at)

    formatted_created_at.short_description = "Ngày tạo"


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "product",
        "quantity",
        "id",
    )
    list_filter = ("order", "product")
    search_fields = ("order__user__username", "product")
    ordering = ("-created_at",)


admin.site.register(Tag, TagAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Blog, BlogAdmin)
