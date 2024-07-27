from django.urls import path

from bts_info.views import BtsInfo

urlpatterns = [
    path('', BtsInfo.as_view(), name='bts-info'),
]
