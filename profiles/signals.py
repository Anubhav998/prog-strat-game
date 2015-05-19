from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from profiles.models import Profile


@receiver(post_save, sender=User)
def arena_post_save(sender, instance, created, **kwargs):
    """
    When a new user is created, create a profile
    """
    if created:
        Profile.objects.create(user=instance)
