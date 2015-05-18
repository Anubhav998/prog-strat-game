from django.test import TestCase
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from sciences.models import Technology, Benefit, ResourceBenefit
from resources.models import Resource


class TechnologyTestCase(TestCase):
    fixtures = []

    def setUp(self):
        self.technology = Technology.objects.create(name="test_tech")

    def test_resource_unicode_method(self):
        self.assertEquals(self.technology.__unicode__(), "test_tech")

    def test_benefit_unicode_method(self):
        self.benefit = Benefit(
            technology=self.technology,
            amount=100,
            modifier="+"
        )
        self.assertEquals(self.benefit.__unicode__(), "+100")

    def test_resource_benefit_unicode_method(self):
        self.resource = Resource.objects.create(name='fuel')
        self.resource_benefit = ResourceBenefit.objects.create(
            resource=self.resource,
            technology=self.technology,
            amount=100,
            modifier="+"
        )
        self.assertEquals(self.resource_benefit.__unicode__(), "test_tech (+100 fuel)")


class ResourceAPITestCase(APITestCase):
    fixtures = []

    def setUp(self):
        self.username = get_random_string(10)
        self.user = User.objects.create_superuser(username=self.username, email="test@test.com", password="test")
        auth = self.client.login(username=self.username, password='test')
        self.assertTrue(auth)

    def test_resource_list(self):
        url = reverse('resource-list')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
