from rest_framework.filters import BaseFilterBackend
from .models import Master


class PermissionFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user:
            user = request.user
            if user.is_staff:
                return queryset.all()
            elif Master.objects.filter(user=user).exists():
                return queryset.filter(executor__user__username=user)
            else:
                return queryset.filter(client__username=user)


                