from django.urls import path

from bts_files.views import BtsFiles, KmlOnly

urlpatterns = [
    path('', BtsFiles.as_view(), name='bts-files'),
    path('kml/', KmlOnly.as_view(), name='bts-files-kml'),
]
