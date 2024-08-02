from http import HTTPStatus
from pathlib import Path
from unittest.mock import patch

import pytest
from django.urls import reverse_lazy

from neighbors.tests.fixtures.g2g_test_data import enm_g2g_data
from neighbors.tests.fixtures.g2u_test_data import enm_g2u_data
from neighbors.tests.fixtures.network_live_test_data import gsm_network_cells, wcdma_network_cells
from neighbors.tests.fixtures.u2g_test_data import enm_u2g_data
from neighbors.tests.fixtures.u2u_test_data import enm_u2u_data
from neighbors.tests.utils import is_word_in_zip

TEMPL_PATH = Path(__file__).resolve().parent.parent / 'fixtures/g2u.xlsx'
G2U_URL = reverse_lazy('nbr-import', kwargs={'direction': 'G2U'})

directions = [
    'G2G',
    'G2U',
    'G2L',
    'U2U',
    'U2G',
    'U2L',
]


@pytest.mark.parametrize('direction', directions)
def test_nbr_import_get_rnpo_user(client, rnpo_user, get_templates, direction):
    """Test get method of NbrImport view when user is rnpo user."""
    url = reverse_lazy('nbr-import', kwargs={'direction': direction})
    client.login(
        username=rnpo_user['username'],
        password=rnpo_user['password'],
    )

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert 'neighbors/import.html' in get_templates(response)


@pytest.mark.parametrize('direction', directions)
def test_nbr_import_post_empty_form(client, rnpo_user, check_message, direction):
    """Test the post method of NbrImport view with empty form."""
    url = reverse_lazy('nbr-import', kwargs={'direction': direction})
    client.login(
        username=rnpo_user['username'],
        password=rnpo_user['password'],
    )
    response = client.post(url, data={})

    assert response.status_code == HTTPStatus.FOUND
    assert check_message(response, 'Submited form is invalid')
    assert response.url == url


@pytest.mark.parametrize(
    'direction, get_enm_data_func_location, enm_data',
    [
        (
            'G2G',
            'neighbors.services.gsm.g2g.main.get_enm_g2g_data',
            enm_g2g_data,
        ),
        (
            'G2U',
            'neighbors.services.gsm.g2u.main.get_enm_g2u_data',
            enm_g2u_data,
        ),
        (
            'U2G',
            'neighbors.services.wcdma.u2g.main.get_enm_u2g_data',
            enm_u2g_data,
        ),
        (
            'U2U',
            'neighbors.services.wcdma.u2u.main.get_u2u_enm_data',
            enm_u2u_data,
        ),
    ],
)
@patch('neighbors.services.network_live.main.DBConnector')
@patch('neighbors.services.network_live.main.GsmTable')
@patch('neighbors.services.network_live.main.WcdmaTable')
def test_nbr_import_post_valid_form(
    MockWcdmaTable,
    MockGsmTable,
    MockDBConnector,
    client,
    rnpo_user,
    direction,
    get_enm_data_func_location,
    enm_data,
):
    """Test the post request of NbrImport view with valid form."""
    input_file = Path(__file__).resolve().parent.parent / f'fixtures/{direction}.xlsx'
    url = reverse_lazy('nbr-import', kwargs={'direction': direction})

    MockDBConnector.get_connection.return_value = None

    if 'G' in direction:
        mock_table = MockGsmTable.return_value
        mock_table.get_enm_cells.return_value = gsm_network_cells
        word_in_text = 'gcell1'
        word_in_excel = 'gcell4'
    else:
        word_in_text = 'ucell1'
        word_in_excel = 'ucell4'

    if 'U' in direction:
        mock_wcdma_table = MockWcdmaTable.return_value
        mock_wcdma_table.get_enm_cells.return_value = wcdma_network_cells

    with patch(get_enm_data_func_location) as mock_get_enm_data:
        mock_get_enm_data.return_value = enm_data
        with open(input_file, 'rb') as temp:
            form_data = {'enm': 'ENM2', 'neighbors_excel': temp}
            client.login(
                username=rnpo_user['username'],
                password=rnpo_user['password'],
            )
            response = client.post(url, data=form_data)

    assert response.status_code == HTTPStatus.OK
    assert response['Content-Disposition'] == f'attachment; filename="{direction}-nbr.zip"'
    assert is_word_in_zip(response.content, 'text', word_in_text)
    assert not is_word_in_zip(response.content, 'text', word_in_excel)
    assert is_word_in_zip(response.content, 'excel', word_in_excel)
