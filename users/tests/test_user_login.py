from http import HTTPStatus

from django.contrib.messages import get_messages
from django.urls import reverse_lazy

from users import views
from users.tests.utils import check_message, fake_is_bind, get_templates

LOGIN_URL = reverse_lazy('login')


def test_get(client):
    """Test the behavior of accessing the login page using the GET method."""
    response = client.get(LOGIN_URL)
    templates = get_templates(response)

    assert response.status_code == HTTPStatus.OK
    assert 'users/login.html' in templates


def test_post_valid_form(client, new_user):
    """Test the behavior of submitting a valid login form."""
    form_data = {
        'username': new_user['username'],
        'password': new_user['password'],
    }
    response = client.post(
        LOGIN_URL,
        data=form_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse_lazy('index')
    assert check_message(response, views.UserLogin.success_message)


def test_post_invalid_form(client, new_user):
    """Test the behavior of submitting an invalid login form with incorrect username."""
    views.is_ldap_bind = fake_is_bind(False)
    invalid_data = {
        'username': new_user['username'],
        'password': 'some-pass',
    }
    error_message = 'Please enter a correct username and password'
    response = client.post(
        LOGIN_URL,
        data=invalid_data,
    )

    assert response.status_code == HTTPStatus.OK
    assert error_message in response.content.decode()


def test_post_user_not_exist(client, new_user):
    """Test the behavior of submitting an invalid login form if user not exists."""
    invalid_data = {
        'username': 'no.user',
        'password': 'some-pass',
    }
    error_message = f"User '{invalid_data['username']}' does not exist. Please register first"

    response = client.post(LOGIN_URL, data=invalid_data)
    messages = list(get_messages(response.wsgi_request))

    assert response.status_code == HTTPStatus.FOUND
    assert any(error_message in str(message) for message in messages), "Flash message not found!"


def test_post_invalid_form_ldap_true(client, django_user_model, new_user):
    """Test the submitting an invalid login form when LDAP binding is simulated as True."""
    views.is_ldap_bind = fake_is_bind(True)
    invalid_data = {
        'username': new_user['username'],
        'password': 'newPass',
    }
    response = client.post(
        LOGIN_URL,
        data=invalid_data,
    )
    user = django_user_model.objects.get(username=new_user['username'])

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse_lazy('index')
    assert check_message(response, views.UserLogin.success_message)
    assert user.check_password(invalid_data['password'])


def test_post_invalid_form_ldap_false(client, new_user):
    """Test the submitting an invalid login form when LDAP binding is simulated as False."""
    views.is_ldap_bind = fake_is_bind(False)
    error_message = 'Please enter a correct username and password'
    invalid_data = {
        'username': new_user['username'],
        'password': 'wrongPass',
    }
    response = client.post(
        LOGIN_URL,
        data=invalid_data,
    )

    assert response.status_code == HTTPStatus.OK
    assert error_message in response.content.decode()
