from django.test import TestCase

from military.models import Category, Unit
from core.defaults import ATTACK, DEFENCE


class MilitaryTestCase(TestCase):
    fixtures = []

    def setUp(self):
        self.category = Category.objects.create(name='testCat')
        self.unit = Unit.objects.create(name="test", category=self.category)

    def test_unit_unicode_method(self):
        self.assertEquals(self.unit.__unicode__(), "test")

    def test_category_unicode_method(self):
        self.assertEquals(self.category.__unicode__(), "testCat")

    def test_unit_get_power_display_method(self):
        self.assertEquals(self.unit.get_power_display(), "({0},{1})".format(ATTACK, DEFENCE))
