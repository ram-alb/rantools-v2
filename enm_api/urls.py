from django.urls import path

from enm_api.views import BscTg, CreateObject

urlpatterns = [
    path('tg-list/', BscTg.as_view()),
    path('create-object/', CreateObject.as_view()),
]
