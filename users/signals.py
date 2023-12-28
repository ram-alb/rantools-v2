from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    """Add a new user to the 'Regular Users' group upon user creation."""
    if created:
        common_users, is_created = Group.objects.get_or_create(
            name='Regular Users',
        )
        if is_created:
            instance.groups.add(common_users)
