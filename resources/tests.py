from django.test import TestCase
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from resources.models import Resource


class ResourceTestCase(TestCase):
    fixtures = []

    def setUp(self):
        self.resource = Resource.objects.create(name="test")

    def test_resource_unicode_method(self):
        self.assertEquals(self.resource.__unicode__(), "test")


class ResourceAPITestCase(APITestCase):
    fixtures = ['resources']

    def setUp(self):
        self.username = get_random_string(10)
        self.user = User.objects.create_superuser(username=self.username, email="test@test.com", password="test")
        auth = self.client.login(username=self.username, password='test')
        self.assertTrue(auth)

    def test_resource_list(self):
        url = reverse('resource-list')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
