from http import HTTPStatus

from django.urls import reverse_lazy


def test_download_gu_template(client, new_user):
    """Test DownloadGUTemplate view."""
    download_url = reverse_lazy('nbr-download-template', kwargs={'direction': 'G2U'})
    client.login(
        username=new_user['username'],
        password=new_user['password'],
    )
    response = client.get(download_url)

    assert response.status_code == HTTPStatus.OK
    assert response['Content-Type'] == 'application/vnd.ms-excel'
    assert response['Content-Disposition'] == 'attachment; filename="G2U.xlsx"'
    assert response.content != b''
