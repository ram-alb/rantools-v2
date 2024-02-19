from http import HTTPStatus

from django.urls import reverse

from users.tests.utils import get_templates

INDEX_URL = reverse('nbr-index')


def test_index_not_logged_in(client):
    """Test neighbor Index view when user is not logged in."""
    response = client.get(INDEX_URL)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('login') + '?next=' + INDEX_URL


def test_index_logged_in(client, new_user):
    """Test neighbor Index view when user is logged in."""
    client.login(
        username=new_user['username'],
        password=new_user['password'],
    )
    response = client.get(INDEX_URL)

    assert response.status_code == HTTPStatus.OK
    assert 'neighbors/index.html' in get_templates(response)
