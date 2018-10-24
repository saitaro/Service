from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Master, Order, Company, Skill
from .filter_backends import PermissionFilterBackend
from .filters import OrderFilter
from .permissions import ClientPermission
from .serializers import (UserSerializer, CompanySerializer, MasterSerializer,
                          SkillSerializer, OrderSerializer)


class RegistrationView(APIView):
    permission_classes = AllowAny,

    def get(self, request, format=None):
        return redirect('/')
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = AllowAny,
        else:
            permission_classes = IsAuthenticated,
        return [permission() for permission in permission_classes]


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


