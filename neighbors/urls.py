from django.urls import path

from neighbors.views import DownloadTemplate, GsmToUmtsNbr, Index

urlpatterns = [
    path('', Index.as_view(), name='nbr-index'),
    path('g2u/', GsmToUmtsNbr.as_view(), name='nbr-g2u'),
    path(
        'download-template/<str:technology>/',
        DownloadTemplate.as_view(),
        name='nbr-download-template',
    ),
]
