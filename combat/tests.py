from django.test import TestCase
from django.contrib.auth.models import User

from combat.models import Conflict, AggressorUnit, DefenderUnit
from military.models import Unit
from arenas.models import Arena


class ConflictTestCase(TestCase):
    fixtures = ['resources', 'technologies', 'military']

    def setUp(self):
        self.user1 = User.objects.create_user(username='test1')
        self.user2 = User.objects.create_user(username='test2')
        self.arena = Arena.objects.create(name="test", created_by=self.user1)
        self.territory = self.arena.territory_set.first()
        self.profile1 = self.user1.profile
        self.profile2 = self.user2.profile
        self.conflict = Conflict.objects.create(
            territory=self.territory,
            aggressor=self.profile1,
            defender=self.profile2,
            start_turn=1
        )
        self.soldier = Unit.objects.get(name='Soldier')

    def test_conflict_unicode_method(self):
        self.assertEquals(self.conflict.__unicode__(), "Conflict")

    def test_conflict_get_total_offence_method(self):
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        self.assertEquals(self.conflict.get_total_offence(), 20)

    def test_conflict_get_total_defence_method(self):
        DefenderUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        DefenderUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        self.assertEquals(self.conflict.get_total_defence(), 20)

    def test_check_complete_method(self):
        self.assertEquals(self.conflict.check_complete(1), True)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        self.assertEquals(self.conflict.check_complete(1), False)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        self.assertEquals(self.conflict.check_complete(1), True)

    def test_conflict_represent_method(self):
        self.assertEquals(self.conflict.represent(), "[]v[]")
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        DefenderUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        self.assertEquals(self.conflict.represent(), "[(10,10),(10,10)]v[(10,10)]")


class ResolveTestCase(TestCase):
    fixtures = ['resources', 'technologies', 'military']

    def setUp(self):
        self.user1 = User.objects.create_user(username='test1')
        self.user2 = User.objects.create_user(username='test2')
        self.arena = Arena.objects.create(name="test", created_by=self.user1)
        self.territory = self.arena.territory_set.first()
        self.profile1 = self.user1.profile
        self.profile2 = self.user2.profile
        self.conflict = Conflict.objects.create(
            territory=self.territory,
            aggressor=self.profile1,
            defender=self.profile2,
            start_turn=1
        )
        self.soldier = Unit.objects.get(name='Soldier')
        self.tank = Unit.objects.get(name="Tank")

    def test_resolve_even_forces(self):
        # aggressor
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        # defender
        DefenderUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        DefenderUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        DefenderUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        DefenderUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        self.conflict.resolve()
        self.assertEquals(self.conflict.represent(), "[]v[]")
        self.assertTrue(self.conflict.check_complete(1))
        self.assertEquals(self.conflict.victory, False)

    def test_resolve_overwhelming_forces(self):
        # aggressor
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        # defender
        DefenderUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        self.conflict.resolve()
        self.assertEquals(self.conflict.represent(), "[(10,10),(10,10),(10,10),(10,10),(10,10)]v[]")
        self.assertTrue(self.conflict.check_complete(1))
        self.assertEquals(self.conflict.victory, True)

    def test_resolve_underwhelming_forces(self):
        # aggressor
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        AggressorUnit.objects.create(conflict=self.conflict, unit=self.soldier)
        # defender
        DefenderUnit.objects.create(conflict=self.conflict, unit=self.tank)
        self.assertEquals(self.conflict.represent(), "[(10,10),(10,10)]v[(10,50)]")
        self.conflict.resolve()
        self.assertEquals(self.conflict.represent(), "[(10,10)]v[(10,50)]")
        self.assertFalse(self.conflict.check_complete(1))
        self.conflict.resolve()
        self.assertEquals(self.conflict.represent(), "[]v[(10,50)]")
        self.assertTrue(self.conflict.check_complete(2))
        self.assertEquals(self.conflict.victory, False)
