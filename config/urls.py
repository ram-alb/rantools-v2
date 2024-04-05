from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from config.views import Index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('api-docs/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api-docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='api-docs'),
    path('users/', include('users.urls')),
    path('neighbors/', include('neighbors.urls')),
    path('enm-api/', include('enm_api.urls')),
]
