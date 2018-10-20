from datetime import datetime, timedelta
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase, force_authenticate
from .factories import MasterFactory, OrderFactory, SkillFactory
from ..models import Order
from ..serializers import OrderSerializer


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
        master = self.master1.user
        self.client.force_authenticate(user=master)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['executor'], master.pk)
        self.assertEqual(response.data[1]['executor'], master.pk)
        
        master = self.master2.user
        self.client.force_authenticate(user=master)
        response = self.client.get(self.url)
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
        user = self.client1
        user.is_staff = True
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        orders = OrderSerializer(Order.objects.all(), many=True,
                                 context={'request': self.client.request})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, orders.data)
        
    def test_unauthorized_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 
                         'Authentication credentials were not provided.')

    def test_user_post(self):
        user = self.client1
        order = {
            'service': self.service1.pk,
            'executor': self.master1.pk,
            'execution_date': datetime.now() + timedelta(days=1)
        }
        self.client.force_authenticate(user=user)
        order_count = Order.objects.count()
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
        self.assertEqual(response.json()['detail'],
                         'You do not have permission to perform this action.')
        
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
        self.assertEqual(response.json()['detail'],
                         'You do not have permission to perform this action.')

    def test_filtered_orders(self):
        client = self.client1
        master = self.master1
        foo = SkillFactory(name='Foo')
        bar = SkillFactory(name='Bar')
        OrderFactory(service=foo, client=client, executor=master)
        OrderFactory(service=foo, client=client)
        OrderFactory(service=bar, client=client)
        self.client.force_authenticate(user=client)
        response = self.client.get(self.url + '?service=Foo&master=' + master.user.username)     
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['service'], foo.pk)
        self.assertEqual(response.data[0]['executor'], master.pk)

    def test_searching_orders(self):
        user = self.client1
        user.is_staff = True
        foo = SkillFactory(name='Comfortably Numb')
        bar = SkillFactory(name='Portably Null')
        OrderFactory(service=foo)
        OrderFactory(service=bar)
        self.client.force_authenticate(user=user)
        
        response = self.client.get(self.url + '?service=Comfortably+Numb')     
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['service'], foo.pk)

        response = self.client.get(self.url + '?service_search=ortably+Nu')     
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['service'], foo.pk)
        self.assertEqual(response.data[1]['service'], bar.pk)


