from django.db.models.signals import post_save
from django.dispatch import receiver

from arenas.models import Arena, Territory


@receiver(post_save, sender=Arena)
def map_post_save(sender, instance, created, **kwargs):
    """
    When a new map is created, create all the child territory squares.
    """
    if created:
        for x in range(int(instance.size_x)):
            for y in range(int(instance.size_y)):
                Territory.objects.create(
                    arena=instance,
                    position_x=x,
                    position_y=y
                )