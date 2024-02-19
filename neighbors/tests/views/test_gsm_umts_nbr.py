from http import HTTPStatus
from pathlib import Path

from django.urls import reverse_lazy

from neighbors.views import g2u
from users.tests.utils import check_message, get_templates

TEMPL_PATH = Path(__file__).resolve().parent.parent / 'fixtures/g2u.xlsx'
G2U_URL = reverse_lazy('nbr-gu', kwargs={'direction': 'G2U'})


def test_get_not_logged_in(client):
    """Test get method of GsmUmtsNbr view when user is not logged in."""
    response = client.get(G2U_URL)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse_lazy('login') + '?next=' + G2U_URL


def test_get_logged_in(client, new_user):
    """Test get method of GsmUmtsNbr view when user is logged in."""
    client.login(
        username=new_user['username'],
        password=new_user['password'],
    )
    response = client.get(G2U_URL)

    assert response.status_code == HTTPStatus.OK
    assert 'neighbors/gu.html' in get_templates(response)


def test_post_g2u_nbr_empty_form(client, new_user):
    """Test post method of GsmUmtsNbr view with invalid form."""
    client.login(
        username=new_user['username'],
        password=new_user['password'],
    )
    response = client.post(G2U_URL, data={})

    assert response.status_code == HTTPStatus.FOUND
    assert check_message(response, 'Submited form is invalid')
    assert response.url == G2U_URL


def test_post_g2u_nbr_valid_form(client, new_user, zip_file):
    """Test post method of GsmUmtsNbr view with valid form."""
    def _fake_generate_report(g2u_neighbors_excel_file):
        return zip_file

    g2u.generate_g2u_nbr_adding_import_report = _fake_generate_report

    client.login(
        username=new_user['username'],
        password=new_user['password'],
    )

    with open(TEMPL_PATH, 'rb') as templ:
        upload_data = {'neighbors_excel': templ}
        response = client.post(G2U_URL, data=upload_data)

    assert response.status_code == HTTPStatus.OK
    assert response['Content-Type'] == 'application/zip'
    assert response['Content-Disposition'] == 'attachment; filename="G2U-nbr.zip"'
