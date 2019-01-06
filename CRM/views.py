from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect

# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, permission_classes
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
    CatalogSerializer,
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
    permission_classes = (IsAuthenticated, ClientPermission)

    """ create() implemented in serializers.OrderSerializer """

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     data = serializer.validated_data
    #     service_id = data.get("service")["id"]
    #     if not Service.objects.filter(id=service_id).exists():
    #         return Response(
    #             data={"No service with id %d provided" % service_id},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #     data["service"] = Service.objects.get(pk=service_id)
    #     data["client_id"] = request.user.id
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(
    #         serializer.data, status=status.HTTP_201_CREATED, headers=headers
    #     )


class UserViewSet(CreationMixin, ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = IsAuthenticated, IsAdminUser
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def create(self, request):
        return super().create_user(request)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = (IsAuthenticated, TokenHasReadWriteScope)


class MasterViewSet(ModelViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    lookup_field = "name"


class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class CatalogView(APIView):
    def get(request, pk):
        queryset = Master.objects.get(pk=pk).catalog
        serializer = CatalogSerializer(catalog, many=True)
        return Response(serializer.data)

