from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration class for the 'users' app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """Connect the 'add_user_to_group' signal to the post_save signal of the User model."""
        from django.contrib.auth.models import User
        from django.db.models.signals import post_save

        from users.signals import add_user_to_group

        post_save.connect(add_user_to_group, sender=User)
