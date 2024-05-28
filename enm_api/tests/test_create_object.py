from unittest.mock import patch
from rest_framework import status
from django.urls import reverse_lazy

URL = reverse_lazy('create-object-api')


def fake_object_data():
    return {
        "enm": "ENM1",
        "subnetwork": "Subnetwork1",
        "sitename": "Site1",
        "platform": "Platform1",
        "oam_ip": "192.168.1.1",
        "technologies": ["LTE"],
    }


def test_create_object_all_technologies(authenticated_client):
    object_data = fake_object_data()
    object_data['technologies'].extend(['GSM', 'UMTS'])
    object_data['rnc'] = 'RNC1'
    object_data['bsc'] = 'BSC1'

    with patch('enm_api.views.create_object', return_value=["Base Station Created"]) as mock_create_object:
        response = authenticated_client.post(URL, object_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == ["Base Station Created"]
        mock_create_object.assert_called_once()

def test_create_object_success(authenticated_client):
    object_data = fake_object_data()
    with patch('enm_api.views.create_object', return_value=["Base Station Created"]) as mock_create_object:
        response = authenticated_client.post(URL, object_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == ["Base Station Created"]
        mock_create_object.assert_called_once()


def test_create_object_invalid_ip(authenticated_client):
    object_data = fake_object_data()
    object_data['oam_ip'] = '999.999.999.999'
    with patch('enm_api.views.create_object', return_value=["Base Station Created"]) as mock_create_object:
        response = authenticated_client.post(URL, object_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "oam_ip" in response.data
        assert response.data["oam_ip"] == ["Invalid IP address format"]
        mock_create_object.assert_not_called()


def test_create_object_no_rnc(authenticated_client):
    object_data = fake_object_data()
    object_data['technologies'].append('UMTS')
    with patch('enm_api.views.create_object', return_value=["Base Station Created"]) as mock_create_object:
        response = authenticated_client.post(URL, object_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'rnc' in response.data
        assert response.data['rnc'] == ["RNC is required if UMTS technology is present."]
        mock_create_object.assert_not_called()


def test_create_object_no_bsc(authenticated_client):
    object_data = fake_object_data()
    object_data['technologies'].append('GSM')
    with patch('enm_api.views.create_object', return_value=["Base Station Created"]) as mock_create_object:
        response = authenticated_client.post(URL, object_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'bsc' in response.data
        assert response.data['bsc'] == ["BSC is required if GSM technology is present."]
        mock_create_object.assert_not_called()
