from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Master


class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        is_master = Master.objects.filter(user=user).exists()
        return request.method in SAFE_METHODS or not (is_master or user.is_staff)

