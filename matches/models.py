from django.db import models
from django.core.exceptions import ValidationError
from reversion import register

from uuidfield import UUIDField

from arenas.models import Arena, Territory
from resources.models import Resource
from military.models import Unit
from sciences.models import Technology


class Match(models.Model):
    arena = models.ForeignKey(Arena)
    player_1 = models.ForeignKey("profiles.Profile", related_name='player_one')
    player_2 = models.ForeignKey("profiles.Profile", related_name='player_two')
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

    def clean(self):
        super(Match, self).clean()
        if self.player_1 is self.player_2:
            raise ValidationError("Player cannot play itself")
        if self.completed and not self.victor:
            raise ValidationError("Completed game must have victor")

    class Meta:
        unique_together = ('player_1', 'player_2', 'uuid')


class Turn(models.Model):
    match = models.ForeignKey(Match, related_name='turns')
    number = models.PositiveIntegerField(default=1)
    profile = models.ForeignKey("profiles.Profile")
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
    object = models.CharField(max_length=64)
    quantity = models.IntegerField(default=0)



class GameState(models.Model):
    match = models.ForeignKey(Match, related_name='states')
    player = models.IntegerField(choices=(
        (1, 'Player One'),
        (2, 'Player Two'),
    ), blank=True, null=True)
    profile = models.ForeignKey("profiles.Profile")

    def __unicode__(self):
        return "{0.match} Game State {0.player}".format(self)

    class Meta:
        unique_together = ('match', 'player',)


class ResourceState(models.Model):
    state = models.ForeignKey(GameState, related_name='resources')
    resource = models.ForeignKey(Resource)
    quantity = models.IntegerField()

    def __unicode__(self):
        return 'Resource State {0.id}'.format(self)

    class Meta:
        unique_together = ("state", "resource",)


class MilitaryState(models.Model):
    state = models.ForeignKey(GameState, related_name='military')
    unit = models.ForeignKey(Unit)
    quantity = models.IntegerField()

    def __unicode__(self):
        return 'Military State {0.id}'.format(self)

    class Meta:
        unique_together = ("state", "unit",)


class TechnologyState(models.Model):
    state = models.ForeignKey(GameState, related_name='technology')
    technology = models.ForeignKey(Technology)
    quantity = models.IntegerField()


    def __unicode__(self):
        return 'Technology State {0.id}'.format(self)

    class Meta:
        unique_together = ("state", "technology",)


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

    def __unicode__(self):
        return 'Territory State {0.id}'.format(self)

    class Meta:
        unique_together = ('state', 'territory')


class Token(models.Model):
    """
    Used for authorizing moves.
    Is unique per game/player. Required for posting updates.
    Is sent back via Status Polling Call.
    """
    uuid = UUIDField(auto=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    match = models.ForeignKey(Match)
    profile = models.ForeignKey("profiles.Profile")

    def __unicode__(self):
        return self.uuid

    class Meta:
        unique_together = ('match', 'profile',)
