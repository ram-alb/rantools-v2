from unittest.mock import patch

from django.urls import reverse_lazy  # type: ignore
from rest_framework import status  # type: ignore

URL = reverse_lazy('create-object-api')

return_value = [
    ('create object', 'done'),
]
response_value = [
    {
        'command': 'create object',
        'output': 'done',
    },
]


def _fake_object_data() -> dict:
    """Return fake BTS object data."""
    return {
        "enm": "ENM1",
        "subnetwork": "Subnetwork1",
        "sitename": "Site1",
        "platform": "Platform1",
        "oam_ip": "192.168.1.1",
        "technologies": ["LTE"],
    }


def test_create_object_all_technologies(authenticated_client):
    """Test creating a BTS object when all technologies are present."""
    object_data = _fake_object_data()
    object_data['technologies'].extend(['GSM', 'UMTS'])
    object_data['rnc'] = 'RNC1'
    object_data['bsc'] = 'BSC1'

    with patch('enm_api.views.create_object', return_value=return_value) as mock_create_object:
        response = authenticated_client.post(URL, object_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == response_value
        mock_create_object.assert_called_once()


def test_create_object_success(authenticated_client):
    """Test creating a BTS object when object data is correct."""
    object_data = _fake_object_data()
    with patch('enm_api.views.create_object', return_value=return_value) as mock_create_object:
        response = authenticated_client.post(URL, object_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == response_value
        mock_create_object.assert_called_once()


def test_create_object_invalid_ip(authenticated_client):
    """Test creating a BTS object when oam ip is incorrect."""
    object_data = _fake_object_data()
    object_data['oam_ip'] = '999.999.999.999'
    with patch('enm_api.views.create_object', return_value=return_value) as mock_create_object:
        response = authenticated_client.post(URL, object_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "oam_ip" in response.data
        assert response.data["oam_ip"] == ["Invalid IP address format"]
        mock_create_object.assert_not_called()


def test_create_object_no_rnc(authenticated_client):
    """Test creating a BTS object without specifying a RNC when UMTS technology is present."""
    object_data = _fake_object_data()
    object_data['technologies'].append('UMTS')
    with patch('enm_api.views.create_object', return_value=return_value) as mock_create_object:
        response = authenticated_client.post(URL, object_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'rnc' in response.data
        assert response.data['rnc'] == ["RNC is required if UMTS technology is present."]
        mock_create_object.assert_not_called()


def test_create_object_no_bsc(authenticated_client):
    """Test creating a BTS object without specifying a BSC when GSM technology is present."""
    object_data = _fake_object_data()
    object_data['technologies'].append('GSM')
    with patch('enm_api.views.create_object', return_value=return_value) as mock_create_object:
        response = authenticated_client.post(URL, object_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'bsc' in response.data
        assert response.data['bsc'] == ["BSC is required if GSM technology is present."]
        mock_create_object.assert_not_called()
