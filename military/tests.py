from django.test import TestCase

from military.models import Category, Unit


class MilitaryTestCase(TestCase):
    fixtures = []

    def setUp(self):
        self.category = Category.objects.create(name='testCat')
        self.unit = Unit.objects.create(name="test", category=self.category)

    def test_unit_unicode_method(self):
        self.assertEquals(self.unit.__unicode__(), "test")

    def test_category_unicode_method(self):
        self.assertEquals(self.category.__unicode__(), "testCat")
