from django import template

register = template.Library()


@register.filter(name='in_group')
def in_group(user, group_name):
    """Check if a user is in the given group."""
    return user.groups.filter(name=group_name).exists()
