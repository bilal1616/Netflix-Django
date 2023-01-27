from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('profiles/', profiles, name="profiles"),
    path('movies/<int:id>', movies, name="movies"),
    path('video/<int:id>', video, name="video"),
    path('search/', search, name='search')
]