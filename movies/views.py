from django.shortcuts import render
from .models import *
from user.models import *
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, 'index.html')

def profiles(request):
    profiles = Profiles.objects.filter(owner = request.user.profil)
    profile = request.user.profil
    context = {
        'profiles': profiles,
        'profile': profile
    }
    return render(request, 'browse.html', context)

def movies(request, id):
    movies = Movie.objects.all()
    profil = Profiles.objects.filter(id = id)
    profiles = Profiles.objects.filter(owner = request.user.profil)
    mypath = request.path[8]
    arama = ''
    if request.GET.get('arama'):
        arama = request.GET.get('arama')
        movies = Movie.objects.filter(
            Q(isim__icontains = arama) |
            Q(kategori__kategori_adi__icontains = arama)
        )
    context = {
        'movies': movies,
        'profil': profil,
        'mypath': mypath,
        'arama': arama,
        'profiles':profiles
    }
    return render(request, 'browse-index.html', context)

def video(request, id):
    film = Movie.objects.filter(id = id)
    context ={
        'film': film
    }
    return render(request, 'video.html', context)

def search(request):
    movies = ''
    arama = ''
    profile = request.user.profil
    if request.GET.get('arama'):
        arama = request.GET.get('arama')
        movies = Movie.objects.filter(
            Q(isim__exact = arama) | # Birebir aynısını yazmamız gerekir
            Q(kategori__kategori_adi__icontains = arama) # Arayacağımız şeyin belli bir kısmını yazmamız yeterli olur
        )
    context = {
        'movies':movies,
        'arama':arama,
        'profile':profile
    }
    return render(request, 'search.html', context)