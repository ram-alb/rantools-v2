from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.views import is_member_pou


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    """Add a new user to the 'Regular Users' group upon user creation."""
    if created:
        is_pou = is_member_pou(instance.email)
        group_regular, _ = Group.objects.get_or_create(name='Regular Users')
        instance.groups.add(group_regular)
        if is_pou:
            group_pou, _ = Group.objects.get_or_create(name='POU Users')
            instance.groups.add(group_pou)
