from http import HTTPStatus

from django.test import Client
from django.urls import reverse_lazy

from network_live.views import excel, select

client = Client()
URL = reverse_lazy('nl-index')


def test_post_request(new_user, mock_select_data, mock_xlsx_file):
    """Test post method of Network Live view."""
    def _fake_select(technologies):
        return mock_select_data

    def _fake_report(network_live_data):
        return mock_xlsx_file

    client.login(
        username=new_user['username'],
        password=new_user['password'],
    )

    req = {'technologies[]': ['gsm', 'nr']}
    techs = req.get('technologies[]')

    select.select_data = _fake_select
    excel.create_excel = _fake_report

    file_name = 'kcell_' + '_'.join(techs) + '_data.xlsx'

    response = client.post(URL, req)

    assert response.status_code == HTTPStatus.OK
    assert response['Content-Type'] == 'application/vnd.ms-excel'
    assert f'attachment; filename="{file_name}"' in response['Content-Disposition']
