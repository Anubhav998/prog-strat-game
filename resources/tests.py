from django.test import TestCase
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from resources.models import Resource, ResourceCost


class ResourceTestCase(TestCase):
    fixtures = []

    def setUp(self):
        self.resource = Resource.objects.create(name="test")

    def test_resource_unicode_method(self):
        self.assertEquals(self.resource.__unicode__(), "test")

    def test_resource_cost_unicode_method(self):
        self.cost = ResourceCost.objects.create(
            base=self.resource,
            resource=self.resource,
            amount=1000
        )
        self.assertEquals(self.cost.__unicode__(), "1000 test")


class ResourceAPITestCase(APITestCase):
    fixtures = ['resources', 'technologies']

    def setUp(self):
        self.username = get_random_string(10)
        self.user = User.objects.create_superuser(username=self.username, email="test@test.com", password="test")
        auth = self.client.login(username=self.username, password='test')
        self.assertTrue(auth)

    def test_resource_list(self):
        url = reverse('resource-list')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
