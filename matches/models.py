from django.db import models

from uuidfield import UUIDField

from profiles.models import Profile
from arenas.models import Arena, Territory
from resources.models import Resource
from military.models import Unit
from sciences.models import Technology


class Match(models.Model):
    arena = models.ForeignKey(Arena)
    player_1 = models.ForeignKey(Profile, related_name='player_one')
    player_2 = models.ForeignKey(Profile, related_name='player_two')
    uuid = UUIDField(auto=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    victor = models.IntegerField(choices=(
        (1, 'Player One'),
        (2, 'Player Two'),
    ), blank=True, null=True)

    def __unicode__(self):
        return "{0.player_1.username}vs{0.player_2.username}[{0.timestamp}]".format(self)

    def get_turn_count(self):
        return self.turns.count()

    class Meta:
        unique_together = ('player_1', 'player_2', 'uuid')


class Turn(models.Model):
    match = models.ForeignKey(Match, related_name='turns')
    number = models.PositiveIntegerField(default=1)
    profile = models.ForeignKey(Profile)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.number = Turn.objects.filter(match=self.match).count() + 1
        super(Turn, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0.match} Turn {0.number}".format(self)

    class Meta:
        unique_together = ('match', 'number',)


class Action(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Move(models.Model):
    turn = models.ForeignKey(Turn, related_name='moves')
    action = models.ForeignKey(Action)
    quantity = models.IntegerField(default=0)

    def __unicode__(self):
        return


class GameState(models.Model):
    match = models.ForeignKey(Match)
    player = models.IntegerField(choices=(
        (0, 'Global'),
        (1, 'Player One'),
        (2, 'Player Two'),
    ), blank=True, null=True)

    def __unicode__(self):
        return "{0.match} Game State {0.player}".format(self)

    class Meta:
        unique_together = ('match', 'player',)


class ResourceState(models.Model):
    state = models.ForeignKey(GameState, related_name='resources')
    resource = models.ForeignKey(Resource)
    quantity = models.IntegerField()


class MilitaryState(models.Model):
    state = models.ForeignKey(GameState, related_name='military')
    unit = models.ForeignKey(Unit)
    quantity = models.IntegerField()


class TechnologyState(models.Model):
    state = models.ForeignKey(GameState, related_name='technology')
    technology = models.ForeignKey(Technology)
    quantity = models.IntegerField()


class TerritoryState(models.Model):
    state = models.ForeignKey(GameState, related_name='territory')
    territory = models.ForeignKey(Territory)
    player = models.IntegerField(choices=(
        (1, 'Player One'),
        (2, 'Player Two'),
    ), blank=True, null=True)
    status = models.CharField(choices=(
        ('owned', "Owned"),
        ('valid', "Valid"),
        ('conflict', "Conflict"),
        ('open', "Open"),
    ), max_length=64)