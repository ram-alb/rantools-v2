from django.urls import path

from neighbors.views import GsmToUmtsNbr, Index

urlpatterns = [
    path('', Index.as_view(), name='nbr-index'),
    path('g2u/', GsmToUmtsNbr.as_view(), name='nbr-g2u'),
]
