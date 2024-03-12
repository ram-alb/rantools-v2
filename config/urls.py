from django.contrib import admin
from django.urls import include, path

from config.views import Index


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('users/', include('users.urls')),
    path('neighbors/', include('neighbors.urls')),
]
