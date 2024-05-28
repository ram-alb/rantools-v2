import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def new_user(db, django_user_model):
    """Fixture for creating a new user."""
    user_data = {
        'username': 'user1',
        'email': 'user1@example.com',
        'password': 'tesT_1234',
    }
    user = django_user_model.objects.create_user(**user_data)
    return user

@pytest.fixture
def token(db, new_user):
    from rest_framework.authtoken.models import Token
    return Token.objects.create(user=new_user)

@pytest.fixture
def authenticated_client(api_client, token):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client

@pytest.fixture
def object_data():
    return {
        "enm": "ENM1",
        "subnetwork": "Subnetwork1",
        "sitename": "Site1",
        "platform": "Platform1",
        "oam_ip": "192.168.1.1",
        "technologies": ["LTE"],
    }
