from datetime import datetime, timedelta

from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework.test import APITestCase, force_authenticate, APIClient

from ..models import Order
from ..serializers import OrderSerializer
from .factories import MasterFactory, OrderFactory, \
                       ServiceFactory, SkillFactory


class OrderTestCase(APITestCase):
    url = reverse('order-list')

    def setUp(self):
        self.client = APIClient()
        self.master1 = MasterFactory()
        self.master2 = MasterFactory()
        self.skill1 = SkillFactory()
        self.skill2 = SkillFactory()
        self.service1 = ServiceFactory(master=self.master1, skill=self.skill1)
        self.service2 = ServiceFactory(master=self.master2, skill=self.skill2)
        self.order1 = OrderFactory(service=self.service1)
        self.order2 = OrderFactory(service=self.service2)
        self.client1 = self.order1.client
        self.client2 = self.order2.client

    def test_masters_orders(self):
        master = self.master1.user
        self.client.force_authenticate(user=master)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['service']['master'], master.username)
        self.assertEqual(response.data[0]['service']['master'], master.username)

        master = self.master2.user
        self.client.force_authenticate(user=master)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['service']['master'], master.username)
        self.assertEqual(response.data[0]['service']['master'], master.username)

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
        orders = OrderSerializer(
            Order.objects.all(), many=True, context={'request': self.client.request}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, orders.data)

    def test_unauthorized_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['detail'], 'Authentication credentials were not provided.'
        )

    def test_user_post(self):
        user = self.client1
        order = {
            'service_id': self.service1.pk,
            'execution_date': datetime.now() + timedelta(days=1),
        }
        bad_order = {
            'service_id': 42,
            'execution_date': datetime.now() + timedelta(days=1),
        }
        bad_order_2 = {
            'service_id': 'foobar',
            'execution_date': datetime.now() + timedelta(days=1),
        }
        self.client.force_authenticate(user=user)
        order_count = Order.objects.count()
        response = self.client.post(self.url, order)
        self.assertEqual(Order.objects.count(), order_count + 1)
        new_order = Order.objects.last()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(new_order.client.username, user.username)
        self.assertEqual(new_order.service.pk, order['service_id'])
        self.assertEqual(
            new_order.execution_date.ctime(), order['execution_date'].ctime()
        )
        bad_order_response = self.client.post(self.url, bad_order)
        self.assertEqual(bad_order_response.status_code, 400)
        self.assertEqual(
            bad_order_response.json()[0], 'No service with id 42 provided.'
        )
        bad_order_response_2 = self.client.post(self.url, bad_order_2)
        self.assertEqual(bad_order_response_2.status_code, 400)
        self.assertEqual(
            bad_order_response_2.json()['service_id'][0], 'A valid integer is required.'
        )

    def test_admin_post(self):
        user = self.client1
        user.is_staff = True
        order = {
            'service_id': self.service2.pk,
            'execution_date': datetime.now() + timedelta(days=1),
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, order)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'],
            'You do not have permission to perform this action.',
        )

    def test_master_post(self):
        user = self.master1.user
        order = {
            'service_id': self.service1.pk,
            'execution_date': datetime.now() + timedelta(days=1),
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, order)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'],
            'You do not have permission to perform this action.',
        )

    def test_filtered_orders(self):
        foo = self.order1
        bar = self.order2
        self.client1.orders.add(self.order2)
        self.client.force_authenticate(user=self.client1)
        response = self.client.get(self.url,{
            'service':foo.service.skill.name,
            'master': foo.service.master.user.username
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['service_id'], foo.pk)
        self.assertEqual(response.data[0]['service']['master'], 
                         foo.service.master.user.username)

    def test_searching_orders(self):
        user = self.client1
        user.is_staff = True
        foo_skill = SkillFactory(name='Comfortably Numb')
        bar_skill = SkillFactory(name='Portably Null')
        foo = ServiceFactory(skill=foo_skill)
        bar = ServiceFactory(skill=bar_skill)
        OrderFactory(service=foo)
        OrderFactory(service=bar)
        self.client.force_authenticate(user=user)

        response = self.client.get(self.url + '?service=Comfortably+Numb')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['service']['id'], foo.pk)

        response = self.client.get(self.url + '?service=ortably+Nu')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['service']['id'], foo.pk)
        self.assertEqual(response.data[1]['service']['id'], bar.pk)


class UserTestCase(APITestCase):
    def test_user_creation(self):
        url = reverse('register')
        data = {'username': 'Feynman', 'password': 'imustbejoking'}
        self.client.post(url, data=data)
        self.assertTrue(User.objects.filter(username='Feynman').exists())
