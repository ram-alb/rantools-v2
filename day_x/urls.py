from django.urls import path
from day_x.views import DayX, LongView

urlpatterns = [
    path('', DayX.as_view(), name='dayX'),
    path('update/', LongView.as_view(), name='update-dayX'),
]
