from django.db.models.signals import post_save
from django.dispatch import receiver

from matches.models import Match, GameState, ResourceState, Turn, TerritoryState
from resources.models import Resource
from arenas.models import Territory
from core.defaults import STARTING


@receiver(post_save, sender=Match)
def match_post_save(sender, instance, created, **kwargs):
    """
    When a new match is created, create the game state objects
    """
    if created:
        # Create Player One Game State Object
        GameState.objects.create(
            match=instance,
            player=1,
            profile=instance.player_1
        )
        # create Player Two Game State Object
        GameState.objects.create(
            match=instance,
            player=2,
            profile=instance.player_2
        )
        # create first turn object
        Turn.objects.create(
            match=instance,
            number=1,
            profile=instance.player_1
        )
        # create the starting territory


@receiver(post_save, sender=GameState)
def game_state_post_save(sender, instance, created, **kwargs):
    """
    When a new Game State is created, initialize the initial values
    """
    if created:
        # starting resources
        for resource, quantity in STARTING['Resources'].iteritems():
            resource = Resource.objects.get(name=resource)
            ResourceState.objects.create(
                resource=resource,
                quantity=quantity,
                state=instance
            )
        # starting positions
        arena = instance.match.arena
        for player, positions in STARTING["Positions"].iteritems():
            for position in positions:
                x, y = arena.normalize(position)
                territory = Territory.objects.get(arena=arena, position_x=x, position_y=y)
                TerritoryState.objects.create(
                    state=instance,
                    territory=territory,
                    player=player,
                    status="owned",
                    is_base=True
                )
