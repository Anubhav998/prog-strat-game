from django.db.models.signals import post_save
from django.dispatch import receiver

from arenas.models import Arena, Territory, TerritoryDetail


@receiver(post_save, sender=Arena)
def arena_post_save(sender, instance, created, **kwargs):
    """
    When a new arena is created, create all the child territory squares.
    """
    if created:
        for x in range(int(instance.size_x)):
            for y in range(int(instance.size_y)):
                Territory.objects.create(
                    arena=instance,
                    position_x=x,
                    position_y=y
                )


@receiver(post_save, sender=Territory)
def territory_post_save(sender, instance, created, **kwargs):
    """
    When a new territory is created, create the associated territory detail
    """
    if created or not instance.territorydetail:
        TerritoryDetail.objects.create(territory=instance)