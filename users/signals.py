from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    """Add a new user to the 'Regular Users' group upon user creation."""
    if created:
        group_name = 'Regular Users'
        try:
            regular_users_group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            regular_users_group = Group.objects.create(name=group_name)
        instance.groups.add(regular_users_group)
