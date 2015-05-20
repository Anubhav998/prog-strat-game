from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from reversion import register

from matches.models import Match


class Profile(models.Model):
    user = models.OneToOneField(User)

    def get_matches(self):
        return Match.objects.filter(Q(player_1=self) | Q(player_2=self))

    def get_completed_matches(self):
        return self.get_matches().filter(completed=True)

    def get_win_count(self):
        return self.player_one.filter(completed=True).filter(victor=1).count() + self.player_two.filter(
            completed=True).filter(victor=2).count()

    def __unicode__(self):
        return self.user.username