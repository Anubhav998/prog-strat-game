from django.db.models.signals import post_save
from django.dispatch import receiver

from arenas.models import Arena, Territory, TerritoryDetail, TerritoryCosts
from core.defaults import TERRITORY_ACQUISITION_COST
from resources.models import Resource


@receiver(post_save, sender=Arena)
def arena_post_save(sender, instance, created, **kwargs):
    """
    When a new arena is created, create all the child territory squares.
    """
    if created and not kwargs.get('raw', False):
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
    if created or not instance.territorydetail and not kwargs.get('raw', False):
        TerritoryDetail.objects.create(territory=instance)


@receiver(post_save, sender=TerritoryDetail)
def territory_detail_post_save(sender, instance, created, **kwargs):
    """
    When a territory detail is created, create a default manpower cost
    """
    if created or instance.costs.count() == 0 and not kwargs.get('raw', False):
        TerritoryCosts.objects.create(
            territory_detail=instance,
            resource=Resource.objects.get(name='Manpower'),
            amount=TERRITORY_ACQUISITION_COST
        )
