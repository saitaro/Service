from django.contrib.auth.models import User
from django.urls import reverse
from random import randint
from datetime import datetime, timedelta
from ..models import Master, Order, Skill
from ..serializers import OrderSerializer
from ..views import OrderViewSet
from .factories import MasterFactory, OrderFactory, UserFactory
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate


class OrdersListTestCase(APITestCase):
    url = api_reverse('order-list')

    def setUp(self):
        self.master1 = MasterFactory()
        self.master2 = MasterFactory()
        self.client1 = OrderFactory(executor=self.master1).client
        self.client2 = OrderFactory(executor=self.master2).client
        self.service1 = OrderFactory(executor=self.master1).service
        self.service2 = OrderFactory(executor=self.master2).service

    def test_masters_orders(self):
        factory = APIRequestFactory()
        request = factory.get(self.url)
        view = OrderViewSet.as_view({'get': 'list'})

        master = self.master1
        force_authenticate(request, user=master.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['executor'], master.pk)
        self.assertEqual(response.data[1]['executor'], master.pk)
            
        master = self.master2
        force_authenticate(request, user=master.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['executor'], master.pk)
        self.assertEqual(response.data[1]['executor'], master.pk)

    def test_clients_orders(self):
        client = self.client1
        self.client.force_authenticate(user=client)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['client'], client.username)
        
        client = self.client2
        self.client.force_authenticate(user=client)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['client'], client.username)

    def test_admin_access(self): 
        factory = APIRequestFactory()
        request = factory.get(self.url)
        user = self.client1
        user.is_staff = True
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        orders = OrderSerializer(Order.objects.all(), many=True, context={'request': request})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, orders.data)
        
    def test_unauthorized_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 
                         'Authentication credentials were not provided.')

    def test_user_post(self):
        order_count = Order.objects.count()
        user = self.client1
        order = {
            'service': self.service1.pk,
            'executor': self.master1.pk,
            'execution_date': datetime.now() + timedelta(days=1)
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, order)
        self.assertEqual(Order.objects.count(), order_count + 1)
        new_order = Order.objects.last()
        self.assertEqual(new_order.client.username, user.username)
        self.assertEqual(new_order.service.pk, order['service'])
        self.assertEqual(new_order.executor.pk, order['executor'])
        self.assertEqual(new_order.execution_date.ctime(), order['execution_date'].ctime())
        
    def test_admin_post(self):
        user = self.client1
        user.is_staff = True
        order = {
            'service': self.service2.pk,
            'executor': self.master1.pk,
            'execution_date': datetime.now() + timedelta(days=1)
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, order)
        self.assertEqual(response.status_code, 403)
        
    def test_master_post(self):
        user = self.master1.user
        order = {
            'service': self.service1.pk,
            'executor': self.master2.pk,
            'execution_date': datetime.now() + timedelta(days=1)
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, order)
        self.assertEqual(response.status_code, 403)


