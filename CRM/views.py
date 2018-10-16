from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from .models import Master, Order, Company, Skill
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework
from .filter_backends import PermissionFilterBackend
from .permissions import ClientPermission
from .serializers import (UserSerializer, CompanySerializer, MasterSerializer,
                          SkillSerializer, OrderSerializer)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = PermissionFilterBackend,

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


