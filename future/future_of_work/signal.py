from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile, Badge


@receiver(post_save, sender=UserProfile)
def assign_default_badge(sender, instance, created, **kwargs):
    """
    Assigns the default badge (rank=1) to a newly created user profile
    """
    if not created:
        return

    try:
        default_badge = Badge.objects.get(rank=1)
        instance.badges.add(default_badge)
    except Badge.DoesNotExist:
        pass
