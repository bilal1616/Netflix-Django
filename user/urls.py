from django.urls import path
from .views import *

urlpatterns = [
    path('login/', userLogin, name="login"),
    path('register/', userRegister, name="register"),
    path('profil/', userProfil, name="profil"),
    path('delete/', userDelete, name="delete"),
    path('logout/', userLogout, name="logout"),
    path('profilcreate/', profilCreate, name="profilcreate"),
    path('acivate<uidb64>/<token>/', activate, name="activate"),
]

# allauth