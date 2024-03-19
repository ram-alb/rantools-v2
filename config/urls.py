from django.contrib import admin
from django.urls import include, path

from config.views import Index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('users/', include('users.urls')),
    path('neighbors/', include('neighbors.urls')),
    path('enm-api/', include('enm_api.urls')),
]
