from http import HTTPStatus

from django.urls import reverse_lazy

from users.tests.utils import get_templates


def test_index_logged_in(client, rnpo_user):
    """Test Network Live Index view when user is logged in."""
    client.login(
        username=rnpo_user['username'],
        password=rnpo_user['password'],
    )
    response = client.get(reverse_lazy('nl-index'))

    assert response.status_code == HTTPStatus.OK
    assert 'network_live/index.html' in get_templates(response)
