from django.urls import path

from enm_api.views import BscTg, Controllers, CreateObject, RncRbsId

urlpatterns = [
    path('tg-list/', BscTg.as_view()),
    path('create-object/', CreateObject.as_view(), name='create-object-api'),
    path('controllers-list/', Controllers.as_view(), name='controllers-list'),
    path('rbsid-map/', RncRbsId.as_view()),
]
