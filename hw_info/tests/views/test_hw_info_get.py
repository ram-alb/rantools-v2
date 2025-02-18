from http import HTTPStatus

from django.urls import reverse_lazy

from users.tests.utils import get_templates


def test_hw_info_get_logged_in(client, rnpo_user):
    """Test HwInfo GET request when user is logged in."""
    client.login(
        username=rnpo_user['username'],
        password=rnpo_user['password'],
    )
    response = client.get(reverse_lazy('hw-info-index'))

    assert response.status_code == HTTPStatus.OK
    assert 'hw_info/index.html' in get_templates(response)
