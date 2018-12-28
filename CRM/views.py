from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect

# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .models import Master, Order, Company, Skill, Service
from .filter_backends import PermissionFilterBackend
from .filters import OrderFilter
from .permissions import ClientPermission
from .mixins import CreationMixin
from .serializers import (
    UserSerializer,
    CompanySerializer,
    MasterSerializer,
    SkillSerializer,
    OrderSerializer,
    PersonnelSerializer,
    CatalogSerializer,
    # ServicesSerializer,
    ServiceSerializer,
)


class RegistrationView(CreationMixin, APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return redirect("/")

    def post(self, request, format=None):
        return super().create_user(request)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = PermissionFilterBackend, DjangoFilterBackend
    filterset_class = OrderFilter

    def get_permissions(self):
        if self.action in ["detail", "list"]:
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = IsAuthenticated, ClientPermission
        return [permission() for permission in permission_classes]


class UserViewSet(CreationMixin, ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def create(self, request):
        return super().create_user(request)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)


class MasterViewSet(ModelViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


@api_view(["GET"])
@permission_classes((AllowAny,))
def catalog(request, pk):
    catalog = Master.objects.get(pk=pk).catalog
    serializer = CatalogSerializer(catalog, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes((AllowAny,))
def services(request):
    services = Service.catalog()
    serializer = ServicesSerializer(services, many=True)
    return Response(serializer.data)

