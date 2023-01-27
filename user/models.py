from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    image = models.FileField(upload_to= 'profil/', verbose_name="Profil Resmi")
    date = models.DateField()
    tc = models.IntegerField(max_length=11)
    tel = models.IntegerField(max_length=11)

    def __str__(self):
        return self.name
class Profiles(models.Model):
    owner = models.ForeignKey(Profil, on_delete=models.CASCADE, null=True)
    isim = models.CharField(max_length=50)
    resim = models.FileField(upload_to= 'profiles/')

    def __str__(self):
        return self.isim



