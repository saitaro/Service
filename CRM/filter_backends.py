from rest_framework.filters import BaseFilterBackend
from .models import Master
from rest_framework import status
from rest_framework.response import Response


class PermissionFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.is_anonymous:
            return queryset.none()
        elif user.is_staff:
            return queryset.all()
        elif Master.objects.filter(user=user).exists():
            return queryset.filter(service__master__user__username=user)
        else:
            return queryset.filter(client__username=user)

