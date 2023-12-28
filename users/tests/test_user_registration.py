from http import HTTPStatus

from django.urls import reverse

from users import views
from users.tests.utils import check_message, fake_is_bind, get_templates

registration_url = reverse('registration')

valid_data = {
    'username': 'user1',
    'email': 'user1@example.com',
    'password1': 'tesT_1234',
    'password2': 'tesT_1234',
}


def test_get(client):
    """Test the behavior of accessing the user registration page using the GET method."""
    response = client.get(registration_url)
    templates = get_templates(response)

    assert response.status_code == HTTPStatus.OK
    assert 'users/registration.html' in templates


def test_post_valid_form_ldap_true(client, django_user_model, check_user):
    """Test the submitting a valid registration form when LDAP binding is simulated as True."""
    users_count_old = django_user_model.objects.count()
    views.is_ldap_bind = fake_is_bind(True)

    response = client.post(
        registration_url,
        data=valid_data,
    )
    users_count_new = django_user_model.objects.count()

    assert users_count_new - users_count_old == 1
    assert check_user(valid_data['username'])

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('login')

    assert check_message(response, views.UserRegistration.success_message)


def test_post_valid_form_ldap_false(client, django_user_model, check_user):
    """Test the submitting a valid registration form when LDAP binding is simulated as False."""
    users_count_old = django_user_model.objects.count()
    views.is_ldap_bind = fake_is_bind(False)

    response = client.post(
        registration_url,
        data=valid_data,
    )

    users_count_new = django_user_model.objects.count()

    assert users_count_new == users_count_old
    assert not check_user(valid_data['username'])

    assert response.status_code == HTTPStatus.OK
    assert views.UserRegistration.error_kcell_message in response.content.decode()


def test_post_invalid_form_wrong_email(client, django_user_model, check_user):
    """Test the behavior of submitting an invalid registration form with an incorrect email."""
    users_count_old = django_user_model.objects.count()

    form_data = {**valid_data, 'email': 'user1@example'}
    response = client.post(
        registration_url,
        data=form_data,
    )

    users_count_new = django_user_model.objects.count()

    assert users_count_new == users_count_old
    assert not check_user(form_data['username'])

    assert response.status_code == HTTPStatus.OK
    assert 'Enter a valid email address.' in response.content.decode()


def test_post_invalid_form_wrong_password(client, django_user_model, check_user):
    """Test the behavior of submitting an invalid registration form with mismatched passwords."""
    users_count_old = django_user_model.objects.count()

    form_data = {**valid_data, 'password2': 'anotherPass'}
    response = client.post(
        registration_url,
        data=form_data,
    )

    users_count_new = django_user_model.objects.count()

    assert users_count_new == users_count_old
    assert not check_user(form_data['username'])

    assert response.status_code == HTTPStatus.OK
    assert 'The two password fields didn’t match.' in response.content.decode()
