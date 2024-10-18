from django import template
from django.shortcuts import resolve_url
from core.models import ShoppingCart

register = template.Library()

NAVBAR_LINKS = [
    {"href": resolve_url("home"), "label": "Trang chủ", "icon": "fa-solid fa-house"},
    {"href": resolve_url("products"), "label": "Sản phẩm", "icon": "fa-solid fa-cubes"},
    {"href": resolve_url("blogs"), "label": "Tin tức", "icon": "fa-solid fa-newspaper"},
    {
        "href": resolve_url("about_us"),
        "label": "Về chúng tôi",
        "icon": "fa-solid fa-circle-info",
    },
]

METADATA = {
    "webname": "Mỹ Phẩm Minh Anh",
    "description": "Cuộc sống với những khoảnh khắc tỏa sáng rực rỡ cùng làn da khỏe mạnh, căng tràn độ ẩm là một khái niệm làm đẹp mới từ Nula Dưỡng ẩm được xem như chiếc chìa khóa thiết yếu giúp làn da tỏa sáng từ bên trong. Mỹ Phẩm Minh Anh với nhiều năm nghiên cứu chuyên sâu về cơ chế giữ ẩm cho làn da dựa trên ý tưởng một làn da căng mọng được cung cấp đầy đủ nước là giải pháp cho nhiều vấn đề về da. Độ ẩm sâu giúp nuôi dưỡng làn da, tăng cường hàng rào bảo vệ da, thanh lọc và duy trì một làn da khoẻ mạnh, trong trẻo và rạng rỡ hơn.",
}


@register.simple_tag
def get_navbar_links():
    return NAVBAR_LINKS


@register.simple_tag
def get_metadata():
    return METADATA


@register.simple_tag(takes_context=True)
def get_total_cart_items(context):
    request = context["request"]
    total_cart_items = ShoppingCart.objects.filter(user=request.user).count()

    return total_cart_items
