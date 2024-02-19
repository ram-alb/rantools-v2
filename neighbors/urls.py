from django.urls import path

from neighbors.views import DownloadGUTemplate, GsmUmtsNbr, Index

urlpatterns = [
    path('', Index.as_view(), name='nbr-index'),
    path('gu/<str:direction>/', GsmUmtsNbr.as_view(), name='nbr-gu'),
    path(
        'download-template/<str:direction>/',
        DownloadGUTemplate.as_view(),
        name='nbr-download-template',
    ),
]
