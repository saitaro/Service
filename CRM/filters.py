from django_filters.rest_framework import FilterSet, CharFilter
from .models import Order


class OrderFilter(FilterSet):
    master = CharFilter(field_name="executor__user__username")
    service = CharFilter(field_name="service__name")

    class Meta:
        model = Order
        fields = 'master', 'service'