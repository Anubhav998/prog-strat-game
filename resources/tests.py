from django.test import TestCase

from resources.models import Resource


class ResourceTestCase(TestCase):
    fixtures = []

    def setUp(self):
        self.resource = Resource.objects.create(name="test")

    def test_injury_unicode_method(self):
        self.assertEquals(self.resource.__unicode__(), "test")