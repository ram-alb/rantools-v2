from django.urls import path

from network_live.views import NetworkLive

urlpatterns = [
    path('', NetworkLive.as_view(), name='network_live'),
]
