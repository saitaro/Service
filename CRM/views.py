from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Master, Order, Company, Skill
from .filter_backends import PermissionFilterBackend
from .filters import OrderFilter
from .permissions import ClientPermission
from .serializers import (UserSerializer, CompanySerializer, MasterSerializer,
                          SkillSerializer, OrderSerializer)


def registration(request):
    if request.method == 'POST':
        user = User.objects.create(
            username=request.POST['user'],
            password=request.POST['password'],
        )
        user.save()
    return redirect('/')


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = PermissionFilterBackend, DjangoFilterBackend
    filterset_class = OrderFilter
    # filterset_fields = 'service__name', 'executor__user__username'

    # def get_queryset(self):
    #     service = self.request.query_params.get('service')
    #     master = self.request.query_params.get('master')
    #     condition = []
    #     if service:
    #         condition.append(Q(service__name=service))
    #     if master:
    #         condition.append(Q(executor__user__username=master))
    #     return self.queryset.filter(*condition) 

    def get_permissions(self):
        if self.action in ['detail', 'list']:
            permission_classes = IsAuthenticated,
        else:
            permission_classes = IsAuthenticated, ClientPermission
        return [permission() for permission in permission_classes]


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = IsAuthenticated,


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = IsAuthenticated,


class MasterViewSet(ModelViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


