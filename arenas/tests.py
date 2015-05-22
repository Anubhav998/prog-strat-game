from django.test import TestCase
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from core.defaults import ARENA_X, ARENA_Y
from arenas.models import Arena, Terrain, TerritoryResource
from resources.models import Resource


class ArenaTestCase(TestCase):
    fixtures = ['resources', 'technologies']

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

    def test_territory_get_coordinates_method(self):
        self.territory = self.arena.territory_set.first()
        self.assertEquals(self.territory.get_coordinates(), (0, 0))

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


class ArenaNormalizeTestCase(TestCase):
    fixtures = ['resources', 'technologies']

    def setUp(self):
        self.user = User.objects.create(username='test1')
        self.cases = (
            (1, 1),  # 0
            (-1, -1),  # 1
            (1, -1),  # 2
            (-1, 1),  # 3
            (0, 0),  # 4
            (-2, -1),  # 5
            (-1, -2),  # 6
            (5, 4),  # 7
            (100, -100),  # 8
        )

    def test_small_normalize_method(self):
        self.arena = Arena.objects.create(name="small", size_x=5, size_y=5, created_by=self.user)
        self.assertEquals(self.arena.normalize(self.cases[0]), (1, 1))
        self.assertEquals(self.arena.normalize(self.cases[1]), (4, 4))
        self.assertEquals(self.arena.normalize(self.cases[2]), (1, 4))
        self.assertEquals(self.arena.normalize(self.cases[3]), (4, 1))
        self.assertEquals(self.arena.normalize(self.cases[4]), (0, 0))
        self.assertEquals(self.arena.normalize(self.cases[5]), (3, 4))
        self.assertEquals(self.arena.normalize(self.cases[6]), (4, 3))
        self.assertRaises(ValidationError, self.arena.normalize, self.cases[7])
        self.assertRaises(ValidationError, self.arena.normalize, self.cases[8])

    def test_normal_normalize_method(self):
        self.arena = Arena.objects.create(name='normal', created_by=self.user)
        self.assertEquals(self.arena.normalize(self.cases[0]), (1, 1))
        self.assertEquals(self.arena.normalize(self.cases[1]), (15, 15))
        self.assertEquals(self.arena.normalize(self.cases[2]), (1, 15))
        self.assertEquals(self.arena.normalize(self.cases[3]), (15, 1))
        self.assertEquals(self.arena.normalize(self.cases[4]), (0, 0))
        self.assertEquals(self.arena.normalize(self.cases[5]), (14, 15))
        self.assertEquals(self.arena.normalize(self.cases[6]), (15, 14))
        self.assertEquals(self.arena.normalize(self.cases[7]), (5, 4))
        self.assertRaises(ValidationError, self.arena.normalize, self.cases[8])

    def test_large_normalize_method(self):
        self.arena = Arena.objects.create(name='large', size_x=25, size_y=25, created_by=self.user)
        self.assertEquals(self.arena.normalize(self.cases[0]), (1, 1))
        self.assertEquals(self.arena.normalize(self.cases[1]), (24, 24))
        self.assertEquals(self.arena.normalize(self.cases[2]), (1, 24))
        self.assertEquals(self.arena.normalize(self.cases[3]), (24, 1))
        self.assertEquals(self.arena.normalize(self.cases[4]), (0, 0))
        self.assertEquals(self.arena.normalize(self.cases[5]), (23, 24))
        self.assertEquals(self.arena.normalize(self.cases[6]), (24, 23))
        self.assertEquals(self.arena.normalize(self.cases[7]), (5, 4))
        self.assertRaises(ValidationError, self.arena.normalize, self.cases[8])

    def test_rectangle_normalize_method(self):
        self.arena = Arena.objects.create(name='rect', size_x=10, size_y=5, created_by=self.user)
        self.assertEquals(self.arena.normalize(self.cases[0]), (1, 1))
        self.assertEquals(self.arena.normalize(self.cases[1]), (9, 4))
        self.assertEquals(self.arena.normalize(self.cases[2]), (1, 4))
        self.assertEquals(self.arena.normalize(self.cases[3]), (9, 1))
        self.assertEquals(self.arena.normalize(self.cases[4]), (0, 0))
        self.assertEquals(self.arena.normalize(self.cases[5]), (8, 4))
        self.assertEquals(self.arena.normalize(self.cases[6]), (9, 3))
        self.assertEquals(self.arena.normalize(self.cases[7]), (5, 4))
        self.assertRaises(ValidationError, self.arena.normalize, self.cases[8])


class ArenaAPITestCase(APITestCase):
    fixtures = ['groups', 'resources', 'technologies']

    def setUp(self):
        self.username = get_random_string(10)
        self.user = User.objects.create_superuser(username=self.username, email="test@test.com", password="test")
        self.group = Group.objects.get(name="Staff")
        self.group.user_set.add(self.user)
        self.arena = Arena.objects.create(name="test2", created_by=self.user)
        self.terrain = Terrain.objects.create(name="testTerrain")
        self.resource1 = Resource.objects.get(name="Metal")
        self.resource2 = Resource.objects.get(name="Fuel")
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
