import pytest
from django.contrib.auth.models import User  # type: ignore
from rest_framework.authtoken.models import Token  # type: ignore
from rest_framework.test import APIClient  # type: ignore


@pytest.fixture
def authenticated_client(db: None, django_user_model: User) -> APIClient:
    """Create authenticated api client."""
    api_client = APIClient()

    user_data = {
        'username': 'user1',
        'email': 'user1@example.com',
        'password': 'tesT_1234',
    }
    user = django_user_model.objects.create_user(**user_data)

    token = Token.objects.create(user=user)

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client
