from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from uuidfield import UUIDField

from arenas.models import Arena, Territory
from resources.models import Resource
from military.models import Unit
from sciences.models import Technology
from core.defaults import RELIGION_COST


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
        return "{0.player_1.user.username}.vs.{0.player_2.user.username}".format(self)

    def get_turn_count(self):
        """Returns the number of turns"""
        return self.turns.count()

    def get_current_turn(self):
        """Returns the current turn object"""
        return self.turns.latest('number')

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
    object = models.CharField(max_length=64, default="")
    quantity = models.IntegerField(default=0)


class GameState(models.Model):
    match = models.ForeignKey(Match, related_name='states')
    player = models.IntegerField(choices=(
        (1, 'Player One'),
        (2, 'Player Two'),
    ), blank=True, null=True)
    profile = models.ForeignKey("profiles.Profile", null=True)

    def __unicode__(self):
        return "{0.match} Game State {0.player}".format(self)

    def spend_resources(self, costs, quantity, commit=False):
        """Spend a list of resources times a quantity

        :param costs: list of `matches.ResourceCost` objects
        :param quantity: number of units to
        :param commit: Boolean, defaults to true. If false, it will commit changes
        :return: True or ValidationError
        """
        for cost in costs:
            resource_state, _ = ResourceState.objects.get_or_create(state=self, resource=cost.resource)
            resource_state.quantity -= cost.amount * quantity
            resource_state.clean()
            if commit:
                resource_state.save()
        return True

    def check_tech(self, dependencies):
        """Checks to see if the necessary tech is acquired

        :param dependencies: a list of technology dependency objects
        :return: Tuple, Boolean, missing
        """
        states = []
        missing = []
        for dependency in dependencies:
            technology_state, _ = TechnologyState.objects.get_or_create(state=self, technology=dependency.technology)
            states.append(technology_state.acquired)
            if not technology_state.acquired:
                missing.append(technology_state.technology.name)
        return all(states), missing

    def sync_territories(self):
        """Syncs the two game states territory states
        :return: Boolean
        """
        for territory_state in self.territory.all():
            territory_state.sync()

    def produce_resources(self, player, commit=False):
        """Loops over territory and produces the turns resources

        :param player: Int - select which player's resources should be generated
        :param commit: Boolean - if True, will apply changes
        :return: Boolean
        """
        for territory_state in self.territory.filter(player=player):
            detail = territory_state.territory.territorydetail
            for product in detail.produces.all():
                resource_state, _ = ResourceState.objects.get_or_create(state=self, resource=product.resource)
                resource_state.quantity += product.amount
                if commit:
                    resource_state.save()
        return True

    def apply_turn(self, turn, commit=False):
        """Applies a turn to the current game state. If validate is false, the changes will actually apply.

        :param turn: `matches.Turn` object to apply
        :param commit: Boolean - if True, changes will apply and it will return a validation error or True
        :return: True if everything has successfully applied
        """
        for move in turn.moves.all():
            if move.action.name == "Refine":
                try:
                    resource = Resource.objects.get(name=move.object)
                except ObjectDoesNotExist:
                    raise ValidationError('invalid resource name: "{0.object}"'.format(move))
                tech, missing = self.check_tech(resource.dependencies.all())
                if not tech:
                    raise ValidationError('insufficient technology: {0}'.format(",".join(missing)))
                self.spend_resources(resource.costs.all(), move.quantity, commit)
                new_resource_state, _ = ResourceState.objects.get_or_create(state=self, resource=resource)
                new_resource_state.quantity += move.quantity
                new_resource_state.clean()
                if commit:
                    new_resource_state.save()
            elif move.action.name == "Purchase":
                try:
                    unit = Unit.objects.get(name=move.object)
                except ObjectDoesNotExist:
                    raise ValidationError('invalid unit name: "{0.object}"'.format(move))
                tech, missing = self.check_tech(unit.dependencies.all())
                if not tech:
                    raise ValidationError('insufficient technology: {0}'.format(",".join(missing)))
                self.spend_resources(unit.costs.all(), move.quantity, commit)
                military_state, _ = MilitaryState.objects.get_or_create(state=self, unit=unit)
                military_state.quantity += move.quantity
                military_state.clean()
                if commit:
                    military_state.save()
            elif move.action.name == "Research":
                try:
                    technology = Technology.objects.get(name=move.object)
                except ObjectDoesNotExist:
                    raise ValidationError('invalid technology name: "{0.object}"'.format(move))
                tech, missing = self.check_tech(technology.dependencies.all())
                if not tech:
                    raise ValidationError('insufficient technology: {0}'.format(",".join(missing)))
                self.spend_resources(technology.costs.all(), 1, commit)
                technology_state, _ = TechnologyState.objects.get_or_create(state=self, technology=technology)
                technology_state.acquired = True
                if commit:
                    technology_state.save()
            elif move.action.name == "Pray":
                manpower = Resource.objects.get(name="Manpower")
                resource_state, c = ResourceState.objects.get_or_create(state=self, resource=manpower)
                resource_state.quantity -= RELIGION_COST * move.quantity
                resource_state.clean()
                if commit:
                    resource_state.save()
                religion_state, _ = ReligionState.objects.get_or_create(state=self)
                religion_state.amount += move.quantity
                religion_state.clean()
                if commit:
                    religion_state.save()
                    # elif move.action.name is "Claim":
                    #     pass
                    # elif move.action.name is "Invade":
                    #     pass
        return True

    class Meta:
        unique_together = ('match', 'player',)


class ResourceState(models.Model):
    """Model for storing the state of various resources for a player in game"""
    state = models.ForeignKey(GameState, related_name='resources')
    resource = models.ForeignKey(Resource)
    quantity = models.IntegerField(default=0)

    def clean(self):
        super(ResourceState, self).clean()
        if self.quantity < 0:
            raise ValidationError('insufficent {0.resource.name}'.format(self))

    def __unicode__(self):
        return 'Resource State {0.id}'.format(self)

    class Meta:
        unique_together = ("state", "resource",)


class MilitaryState(models.Model):
    state = models.ForeignKey(GameState, related_name='military')
    unit = models.ForeignKey(Unit)
    quantity = models.IntegerField(default=0)

    def clean(self):
        super(MilitaryState, self).clean()
        if self.quantity < 0:
            raise ValidationError('Cannot have less than 0 units')

    def __unicode__(self):
        return 'Military State {0.id}'.format(self)

    class Meta:
        unique_together = ("state", "unit",)


class TechnologyState(models.Model):
    state = models.ForeignKey(GameState, related_name='technology')
    technology = models.ForeignKey(Technology)
    acquired = models.BooleanField(default=False)

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
    ), max_length=64, default="open")
    is_base = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Territory State {0.id}'.format(self)

    def get_other(self):
        player = 1 if self.player == 2 else 2
        match = self.state.match
        other_state = GameState.objects.get(
            match=match,
            player=player
        )
        other_territory_state, _ = TerritoryState.objects.get_or_create(
            state=other_state,
            territory=self.territory
        )
        return other_territory_state

    def sync(self):
        other = self.get_other()
        if other and other.status != self.status:  # pragma: no cover
            other.status = self.status
            other.save()

    class Meta:
        unique_together = ('state', 'territory')


class ReligionState(models.Model):
    state = models.ForeignKey(GameState, related_name='religion')
    amount = models.IntegerField(default=0)

    def __unicode__(self):
        return "Faith State {0.id}".format(self)


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
        return str(self.uuid)

    class Meta:
        unique_together = ('match', 'profile',)
