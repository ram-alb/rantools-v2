from django.urls import path

from users.views import UserLogin, UserLogout, UserRegistration

urlpatterns = [
    path('create/', UserRegistration.as_view(), name='registration'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
]
