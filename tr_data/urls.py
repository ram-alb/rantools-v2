from django.urls import path

from tr_data.views import TrData

urlpatterns = [
    path('', TrData.as_view(), name='tr-data-index'),
]
