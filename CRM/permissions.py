from rest_framework.permissions import BasePermission
from .models import Master


class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        is_master = Master.objects.filter(user=user).exists()
        return not (is_master or user.is_staff)


        