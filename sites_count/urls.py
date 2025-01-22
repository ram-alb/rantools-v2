from django.urls import path

from sites_count.views import SitesCountView

urlpatterns = [
    path('', SitesCountView.as_view(), name='sites_count'),
]
