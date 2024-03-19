from django.urls import path

from enm_api.views import BscTg

urlpatterns = [
    path('tg-list/', BscTg.as_view()),
]
