from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from profiles.models import Profile


class ProfileTestCase(TestCase):
    fixtures = []

    def setUp(self):
        self.username = get_random_string(10)
        self.user = User.objects.create_superuser(username=self.username, email="test@test.com", password="password")
        self.profile = self.user.profile

    def test_profile_unicode_method(self):
        self.assertEquals(self.profile.__unicode__(), self.username)

    def test_profile_get_matches_method(self):
        self.assertEquals(self.profile.get_matches().count(), 0)

    def test_profile_get_completed_matches_method(self):
        self.assertEquals(self.profile.get_completed_matches().count(), 0)

    def test_profile_get_win_count_method(self):
        self.assertEquals(self.profile.get_win_count(), 0)
