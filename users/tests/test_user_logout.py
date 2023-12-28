from http import HTTPStatus

from django.urls import reverse

from users.tests.utils import check_message
from users.views import UserLogout

LOGOUT_URL = reverse('logout')


def test_logout(client, new_user):
    """Test the behavior of logging out a user."""
    client.login(
        username=new_user['username'],
        password=new_user['password'],
    )

    response = client.post(LOGOUT_URL)

    assert response.status_code == HTTPStatus.FOUND
    assert check_message(response, UserLogout.success_message)
