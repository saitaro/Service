from django_filters.rest_framework import FilterSet, CharFilter
from .models import Order


class OrderFilter(FilterSet):
    master = CharFilter(
        label="Master",
        field_name="service__master__user__username",
        lookup_expr="icontains",
    )
    service = CharFilter(
        label="Service", field_name="service__skill__name", lookup_expr="icontains"
    )

    class Meta:
        model = Order
        fields = "master", "service"

