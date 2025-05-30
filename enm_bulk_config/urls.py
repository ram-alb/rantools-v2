from django.urls import path

from enm_bulk_config.views import EnmBulkConfigView, download_template

urlpatterns = [
    path("", EnmBulkConfigView.as_view(), name="enm_bulk_config"),
    path(
        "download-template/",
        download_template,
        name="enm_bulk_config_download_template",
    ),
]
