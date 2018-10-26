# from django.conf.urls import url, include
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers, serializers, viewsets
from CRM.views import (UserViewSet, CompanyViewSet, MasterViewSet,
                       SkillViewSet, OrderViewSet, RegistrationView)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'masters', MasterViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'), name='api'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('regi/', UserViewSet.as_view({'post': 'create'}), name='user-create'),
]


