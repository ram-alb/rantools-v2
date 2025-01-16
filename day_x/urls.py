from django.urls import path

from day_x.views import DayXIndexView, UpdateDayXFileView

urlpatterns = [
    path('', DayXIndexView.as_view(), name='dayX'),
    path('update/', UpdateDayXFileView.as_view(), name='update-dayX'),
]
