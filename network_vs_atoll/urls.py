from django.urls import path

from network_vs_atoll.views import NetworkVsAtollView

urlpatterns = [
    path('', NetworkVsAtollView.as_view(), name='network_vs_atoll'),
]
