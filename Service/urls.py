from django.conf.urls import url, include
# from django.urls import path, include
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
    url('^', include(router.urls)),
    url('^admin/', admin.site.urls),
    url('^api-auth/', include('rest_framework.urls'), name='api'),
    url('^register/', RegistrationView.as_view(), name='register'),
    url('^regi/', UserViewSet.as_view({'post': 'create'}), name='user-create'),
]


