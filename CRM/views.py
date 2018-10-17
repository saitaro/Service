from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Master, Order, Company, Skill
from .filter_backends import PermissionFilterBackend
from .permissions import ClientPermission
from .serializers import (UserSerializer, CompanySerializer, MasterSerializer,
                          SkillSerializer, OrderSerializer)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_fields = 'service__name',
    filter_backends = PermissionFilterBackend, DjangoFilterBackend
    
    def get_queryset(self):
        service = self.request.query_params.get('service')
        if service:
            return Order.objects.filter(service__name=service)
        return Order.objects.all()

    def get_permissions(self):
        if self.action in ['detail', 'list']:
            permission_classes = IsAuthenticated,
        else:
            permission_classes = IsAuthenticated, ClientPermission
        return [permission() for permission in permission_classes]


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class MasterViewSet(ModelViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer

    def get_master(self):
        return Master.objects.get(pk=self.pk)


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


