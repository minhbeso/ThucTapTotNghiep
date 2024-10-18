import django_filters
from django.db.models import F
from .models import Product, Category, Brand
from .enums import PRODUCT_ORDERINGS, ProductStatus


def categories(request):
    if request is None:
        return Category.objects.none()

    return Category.objects.all()


def brands(request):
    if request is None:
        return Brand.objects.none()

    return Brand.objects.all()


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=categories)
    brand = django_filters.ModelChoiceFilter(queryset=brands)

    order = django_filters.OrderingFilter(
        choices=PRODUCT_ORDERINGS,
    )
    status = django_filters.ChoiceFilter(
        choices=ProductStatus.choices,
        method="filter_by_status",
        label="Trạng thái",
    )

    def filter_by_status(self, queryset, name, value):
        if value == ProductStatus.ON_SALE:
            return queryset.filter(old_price__isnull=False, price__lt=F("old_price"))
        elif value == ProductStatus.IN_STOCK:
            return queryset.filter(quantity__gt=0)
        return queryset
