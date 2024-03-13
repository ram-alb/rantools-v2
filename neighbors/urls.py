from django.urls import path

from neighbors.views import DownloadTemplate, Index, NbrImport

urlpatterns = [
    path('', Index.as_view(), name='nbr-index'),
    path('<str:direction>/', NbrImport.as_view(), name='nbr-import'),
    path(
        'download-template/<str:direction>/',
        DownloadTemplate.as_view(),
        name='nbr-download-template',
    ),
]
