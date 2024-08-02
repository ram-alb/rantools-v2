from http import HTTPStatus

import pytest
from django.urls import reverse_lazy

from services.mixins import LoginMixin


@pytest.mark.parametrize('url', [
    reverse_lazy('bts-files'),
    reverse_lazy('bts-info'),
    reverse_lazy('nbr-index'),
    reverse_lazy('nl-index'),
    reverse_lazy('nbr-import', kwargs={'direction': 'G2U'}),
    reverse_lazy('nbr-download-template', kwargs={'direction': 'G2U'}),
])
def test_get_not_logged_in(client, check_message, url):
    """Test that GET requests to specified URLs when the user is not logged in."""
    response = client.get(url)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse_lazy('login') + '?next=' + url
    assert check_message(response, LoginMixin.not_signed_in_msg)


@pytest.mark.parametrize('url', [
    reverse_lazy('bts-files'),
    reverse_lazy('nbr-index'),
    reverse_lazy('nl-index'),
    reverse_lazy('nbr-import', kwargs={'direction': 'G2U'}),
    reverse_lazy('nbr-download-template', kwargs={'direction': 'G2U'}),
])
def test_get_regular_user(client, regular_user, check_message, url):
    """Test that GET requests to specified URLs without permissions for regular user."""
    client.login(
        username=regular_user['username'],
        password=regular_user['password'],
    )
    response = client.get(url)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse_lazy('index')
    assert check_message(response, LoginMixin.no_permission_msg)
