from http import HTTPStatus

from django.urls import reverse_lazy

from users.tests.utils import get_templates


def test_tr_data_get_logged_in(client, rnpo_user):
    """Test TrData GET request when user is logged in."""
    client.login(
        username=rnpo_user['username'],
        password=rnpo_user['password'],
    )
    response = client.get(reverse_lazy('tr-data-index'))

    assert response.status_code == HTTPStatus.OK
    assert 'tr_data/index.html' in get_templates(response)
