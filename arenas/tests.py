from django.test import TestCase
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from core.defaults import TERRITORY_ACQUISITION_COST, ARENA_X, ARENA_Y
from arenas.models import Arena, Terrain, TerritoryResource
from resources.models import Resource


class ArenaTestCase(TestCase):
    fixtures = []

    def setUp(self):
        self.username = get_random_string(10)
        self.user = User.objects.create_superuser(username=self.username, email="test@test.com", password="test")
        self.arena = Arena.objects.create(name="test", created_by=self.user)

    def test_arena_unicode_method(self):
        self.assertEquals(self.arena.__unicode__(), "test")

    def test_arena_get_size_display_method(self):
        self.assertEquals(self.arena.get_size_display(), "%sx%s" % (ARENA_X, ARENA_Y))

    def test_arena_territory_creation(self):
        self.assertEquals(self.arena.territory_set.count(), ARENA_X * ARENA_Y)

    def test_territory_unicode_method(self):
        self.territory = self.arena.territory_set.first()
        self.assertEquals(self.territory.__unicode__(), "test - (0,0)")

    def test_territory_get_position_display_method(self):
        self.territory = self.arena.territory_set.first()
        self.assertEquals(self.territory.get_position_display(), "0,0")

    def test_territory_create_territory_detail(self):
        self.territory = self.arena.territory_set.first()
        self.assertEquals(self.territory.territorydetail.cost, TERRITORY_ACQUISITION_COST)

    def test_territory_detail_unicode_method(self):
        self.territory = self.arena.territory_set.first()
        self.assertEquals(self.territory.territorydetail.__unicode__(), "test - (0,0) detail")

    def test_territory_detail_resource_unicode_method(self):
        self.territory = self.arena.territory_set.first()
        self.detail = self.territory.territorydetail
        self.territory_resource = TerritoryResource.objects.create(
            territory_detail=self.detail,
            resource=Resource.objects.create(name='fuel'),
            amount=100
        )
        self.assertEquals(self.territory_resource.__unicode__(), "test - (0,0) fuel")

    def test_terrain_unicode_method(self):
        self.terrain = Terrain.objects.create(name='test')
        self.assertEquals(self.terrain.__unicode__(), 'test')


class ArenaAPITestCase(APITestCase):
    fixtures = ['groups']

    def setUp(self):
        self.username = get_random_string(10)
        self.user = User.objects.create_superuser(username=self.username, email="test@test.com", password="test")
        self.group = Group.objects.get(name="Staff")
        self.group.user_set.add(self.user)
        self.arena = Arena.objects.create(name="test2", created_by=self.user)
        self.terrain = Terrain.objects.create(name="testTerrain")
        self.resource1 = Resource.objects.create(name="Metal")
        self.resource2 = Resource.objects.create(name="Fuel")
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

    def test_territory_detail_retrieve(self):
        territory = self.arena.territory_set.first()
        url = reverse('arena-territory-detail', args=(self.arena.id, territory.id))
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_territory_detail_update(self):
        territory = self.arena.territory_set.first()
        url = reverse('arena-territory-detail', args=(self.arena.id, territory.id))
        data = {
            "cost": 400,
            "terrain": self.terrain.id,
            "resources": [
                {
                    "id": self.resource1.id,
                    "name": "Metal",
                    "value": 400
                },
                {
                    "id": self.resource2.id,
                    "name": "Fuel",
                    "value": 600
                }
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)