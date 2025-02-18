from django.urls import path

from hw_info.views import HwInfo

urlpatterns = [
    path('', HwInfo.as_view(), name='hw-info-index'),
]
