from django.urls import path

from toa_submit.services.get_gsm_data import get_site_gsm_name
from toa_submit.views import SearchView, SiteView

urlpatterns = [
    path('', SearchView.as_view(), name='search_form'),
    path('create/', SiteView.as_view(), name='site_form'),
    path('api/get-site-name/', get_site_gsm_name, name='get_site_name'),
]
