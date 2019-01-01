# from django.conf.urls import url, include
from django.urls import path, include
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken import views
from CRM.views import (
    UserViewSet,
    CompanyViewSet,
    MasterViewSet,
    SkillViewSet,
    OrderViewSet,
    ServiceViewSet,
    RegistrationView,
    CatalogView,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"companies", CompanyViewSet)
router.register(r"masters", MasterViewSet)
router.register(r"skills", SkillViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"services", ServiceViewSet)

urlpatterns = [
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path("", include(router.urls)),
    path("swagger/", get_swagger_view(title="Service API")),
    path("docs/", include_docs_urls(title="Service API")),
    path("login/", views.obtain_auth_token, name="login"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls"), name="api"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("catalog/<pk>/", CatalogView.as_view(), name="catalog"),
]

