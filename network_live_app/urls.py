from django.urls import path

from network_live_app.views import NetworkLive

urlpatterns = [
    path('', NetworkLive.as_view(), name='nl-index'),
]
