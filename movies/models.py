from django.db import models

# Create your models here.
class Kategori(models.Model):
    kategori_adi = models.CharField(max_length=50)
    def __str__(self):
        return self.kategori_adi
class Movie(models.Model):
    isim = models.CharField(max_length=200)
    resim = models.FileField(upload_to='filmler/', null=True)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, null=True)
    video = models.FileField(upload_to='videolar/', null=True)
    def __str__(self):
        return self.isim