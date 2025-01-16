from http import HTTPStatus
from unittest.mock import patch

import pytest
from django.urls import reverse_lazy

from bts_info.services.atoll.gsm import AtollGsmCell, NetworkGsmCell
from bts_info.views import BtsInfo

URL = reverse_lazy('bts-info')

lat = 44.57305583
lon = 78.44177778

gsm_atoll_data = [
    AtollGsmCell(
        site='GSite1',
        cell='Gcell1',
        latitude=lat,
        longitude=lon,
        antenna_type='ant_type',
        height=10,
        azimut=10,
        band='GSM 900',
        location='BSC1',
    ),
    AtollGsmCell(
        site='GSite1',
        cell='Gcell2',
        latitude=lat,
        longitude=lon,
        antenna_type='ant_type',
        height=10,
        azimut=100,
        band='GSM 900',
        location='BSC1',
    ),
]

gsm_network_data = [
    NetworkGsmCell(
        location='BSC1',
        site='GSite1',
        cell='Gcell1',
        cellid=0,
        lac=10,
        longitude=lon,
        latitude=lat,
        sharingtype='',
    ),
    NetworkGsmCell(
        location='BSC1',
        site='GSite1',
        cell='Gcell2',
        cellid=1,
        lac=10,
        longitude=lon,
        latitude=lat,
        sharingtype='',
    ),
]

db_atoll_data = {'GSM': gsm_atoll_data}
db_network_data = {'GSM': gsm_network_data}

empty_db_data = {'GSM': [], 'WCDMA': []}


def test_bts_info_get_regular_user(client, regular_user, get_templates):
    """Test a GET request to the BtsFiles view by an regular user."""
    client.login(
        username=regular_user['username'],
        password=regular_user['password'],
    )
    response = client.get(URL)

    assert response.status_code == HTTPStatus.OK
    assert BtsInfo.template_name in get_templates(response)


@patch('bts_info.services.main.get_mimo_order', return_value={})
@patch('bts_info.services.main.select_db_data')
@pytest.mark.parametrize(
    'db_data, source',
    [(db_atoll_data, 'atoll'), (db_network_data, 'network')],
)
def test_post_request_with_existing_site(
    mock_select_db_data,
    mock_get_mimo_order,
    client,
    regular_user,
    db_data,
    source,
):
    """Test POST request for BtsInfo view with an existing site."""
    form_data = {
        'bts_id': 'GSite1',
        'source': source,
    }
    mock_select_db_data.return_value = db_data

    client.login(
        username=regular_user['username'],
        password=regular_user['password'],
    )

    response = client.post(URL, form_data)

    assert response.status_code == HTTPStatus.OK
    assert b'Gcell2' in response.content
    assert b'GSite1' in response.content


@patch('bts_info.services.main.get_mimo_order', return_value={})
@patch('bts_info.services.main.select_db_data')
@pytest.mark.parametrize('source', ['atoll', 'network'])
def test_post_request_with_non_existing_site(
    mock_select_db_data,
    mock_get_mimo_order,
    client,
    regular_user,
    check_message,
    source,
):
    """Test POST request for BtsInfo view with a non-existing site."""
    form_data = {
        'bts_id': 'GSite1',
        'source': source,
    }

    mock_select_db_data.side_effect = RuntimeError('Site with id GSite1 was not found')

    client.login(
        username=regular_user['username'],
        password=regular_user['password'],
    )

    response = client.post(URL, form_data)

    assert response.status_code == HTTPStatus.OK
    assert check_message(response, 'Site with id GSite1 was not found')
