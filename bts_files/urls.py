from django.urls import path

from bts_files.views import BtsFiles

urlpatterns = [
    path('', BtsFiles.as_view(), name='bts-files'),
]
