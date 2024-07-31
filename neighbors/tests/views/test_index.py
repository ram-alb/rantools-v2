from http import HTTPStatus

from django.urls import reverse_lazy

from neighbors.views import Index

URL = reverse_lazy('nbr-index')


def test_index_logged_in_rnpo_user(client, rnpo_user, get_templates):
    """Test neighbor Index view when user is rnpo user."""
    client.login(
        username=rnpo_user['username'],
        password=rnpo_user['password'],
    )
    response = client.get(URL)

    assert response.status_code == HTTPStatus.OK
    assert Index.template_name in get_templates(response)
