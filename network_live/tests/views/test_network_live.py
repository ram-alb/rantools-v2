from http import HTTPStatus

from django.test import Client
from django.urls import reverse_lazy

from network_live.views import select

client = Client()
URL = reverse_lazy('nl-index')


def test_post_request(rnpo_user, mock_select_data, mock_xlsx_file):
    """Test post method of Network Live view."""
    def _fake_select(technologies):
        return mock_select_data

    select.select_data = _fake_select
    form_data = {'technologies': ['gsm', 'nr']}
    file_name = 'nl_cells.xlsx'

    client.login(
        username=rnpo_user['username'],
        password=rnpo_user['password'],
    )
    response = client.post(URL, data=form_data)

    assert response.status_code == HTTPStatus.OK
    assert response['Content-Type'] == 'application/vnd.ms-excel'
    assert f'attachment; filename="{file_name}"' in response['Content-Disposition']
