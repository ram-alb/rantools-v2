from http import HTTPStatus

from django.urls import reverse

from users.tests.utils import get_templates

INDEX_URL = reverse('nbr-index')


def test_index_not_logged_in(client):
    """Test neighbor Index view when user is not logged in."""
    response = client.get(INDEX_URL)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('login') + '?next=' + INDEX_URL


def test_index_logged_in_regular_user(client, regular_user):
    """Test neighbor Index view when user is regular user."""
    client.login(
        username=regular_user['username'],
        password=regular_user['password'],
    )
    response = client.get(INDEX_URL)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('index')


def test_index_logged_in_rnpo_user(client, rnpo_user):
    """Test neighbor Index view when user is rnpo user."""
    client.login(
        username=rnpo_user['username'],
        password=rnpo_user['password'],
    )
    response = client.get(INDEX_URL)

    assert response.status_code == HTTPStatus.OK
    assert 'neighbors/index.html' in get_templates(response)
