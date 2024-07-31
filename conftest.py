import pytest
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages

user_data = {
    'username': 'user1',
    'email': 'user1@example.com',
    'password': 'tesT_1234',
}


@pytest.fixture
def regular_user(db, django_user_model):
    """Fixture for creating a new regular user."""
    user = django_user_model.objects.create_user(**user_data)
    group, _ = Group.objects.get_or_create(name='Regular Users')

    user.groups.add(group)
    user.save()

    return user_data


@pytest.fixture
def rnpo_user(db, django_user_model):
    """Fixture for creating a new rnpo user."""
    user = django_user_model.objects.create_user(**user_data)
    group, _ = Group.objects.get_or_create(name='RNPO Users')

    user.groups.add(group)
    user.save()

    return user_data


@pytest.fixture
def check_message():
    """Check if a specific message is present in the response's messages."""
    def _check_message(response, message):
        messages = list(get_messages(response.wsgi_request))
        if len(messages) == 1:
            return str(messages[0]) == message
        return False

    return _check_message


@pytest.fixture
def get_templates():
    """Get a list of template names used in the response."""
    def _get_templates(response):
        return [template.name for template in response.templates]
    return _get_templates
