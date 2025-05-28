from django.urls import path
from enm_bulk_config.views import EnmBulkConfigView

urlpatterns = [
    path('', EnmBulkConfigView.as_view(), name='enm_bulk_config'),
]
