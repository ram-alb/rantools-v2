from http import HTTPStatus

import pytest
from django.urls import reverse_lazy


@pytest.mark.parametrize('direction', ['G2U', 'U2G', 'G2L'])
def test_download_template_regular_user(client, regular_user, direction):
    """Test DownloadTemplate view by regular user."""
    download_url = reverse_lazy('nbr-download-template', kwargs={'direction': direction})
    client.login(
        username=regular_user['username'],
        password=regular_user['password'],
    )
    response = client.get(download_url)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse_lazy('index')


@pytest.mark.parametrize('direction', ['G2U', 'U2G', 'G2L'])
def test_download_template_rnpo_user(client, rnpo_user, direction):
    """Test DownloadTemplate view by rnpo user."""
    download_url = reverse_lazy('nbr-download-template', kwargs={'direction': direction})
    client.login(
        username=rnpo_user['username'],
        password=rnpo_user['password'],
    )
    response = client.get(download_url)

    assert response.status_code == HTTPStatus.OK
    assert response['Content-Type'] == 'application/vnd.ms-excel'
    assert response['Content-Disposition'] == f'attachment; filename="{direction}.xlsx"'
    assert response.content != b''
