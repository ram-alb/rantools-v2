from http import HTTPStatus

import pytest
from django.urls import reverse_lazy

from services.mixins import LoginMixin


@pytest.mark.parametrize('url_name', [
    'bts-files',
    'bts-info',
    'nbr-index',
    'nl-index',
])
def test_get_not_logged_in(client, check_message, url_name):
    """Test that GET requests to specified URLs when the user is not logged in."""
    url = reverse_lazy(url_name)
    response = client.get(url)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse_lazy('login') + '?next=' + url
    assert check_message(response, LoginMixin.not_signed_in_msg)


@pytest.mark.parametrize('url_name', [
    'bts-files',
    'nbr-index',
    'nl-index',
])
def test_get_regular_user(client, regular_user, check_message, url_name):
    """Test that GET requests to specified URLs without permissions for regular user."""
    url = reverse_lazy(url_name)
    client.login(
        username=regular_user['username'],
        password=regular_user['password'],
    )
    response = client.get(url)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse_lazy('index')
    assert check_message(response, LoginMixin.no_permission_msg)
