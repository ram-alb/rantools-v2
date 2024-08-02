import pytest

user_data = {
    'username': 'user1',
    'email': 'user1@example.com',
    'password': 'tesT_1234',
}


@pytest.fixture
def new_user(db, django_user_model):
    """Fixture for creating a new user."""
    django_user_model.objects.create_user(**user_data)
    return user_data


@pytest.fixture
def check_user(django_user_model):
    """Fixture for checking the existence of a user."""
    def is_user_exists(username):
        return django_user_model.objects.filter(username=username).exists()
    return is_user_exists
