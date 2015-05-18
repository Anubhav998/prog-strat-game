from django.test import TestCase
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from arenas.models import Arena


class ArenaTestCase(TestCase):
    fixtures = []

    def setUp(self):
        self.username = get_random_string(10)
        self.user = User.objects.create_superuser(username=self.username, email="test@test.com", password="test")
        self.arena = Arena.objects.create(name="test", created_by=self.user)

    def test_arena_unicode_method(self):
        self.assertEquals(self.arena.__unicode__(), "test")

    def test_arena_get_size_display_method(self):
        self.assertEquals(self.arena.get_size_display(), "16x16")

    def test_arena_territory_creation(self):
        self.assertEquals(self.arena.territory_set.count(), 16 * 16)

    def test_territory_unicode_method(self):
        self.territory = self.arena.territory_set.first()
        self.assertEquals(self.territory.__unicode__(), "test - (0,0)")

    def test_territory_get_position_display_method(self):
        self.territory = self.arena.territory_set.first()
        self.assertEquals(self.territory.get_position_display(), "0,0")


class ArenaAPITestCase(APITestCase):
    fixtures = ['groups']

    def setUp(self):
        self.username = get_random_string(10)
        self.user = User.objects.create_superuser(username=self.username, email="test@test.com", password="test")
        self.group = Group.objects.get(name="Staff")
        self.group.user_set.add(self.user)
        self.arena = Arena.objects.create(name="test2", created_by=self.user)
        auth = self.client.login(username=self.username, password='test')
        self.assertTrue(auth)

    def test_arena_list(self):
        url = reverse('arena-list')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_arena_create(self):
        url = reverse('arena-list')
        data = {'name': "Test3"}
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

