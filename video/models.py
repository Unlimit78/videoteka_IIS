

from django.db import models
from django.contrib.auth.models import AbstractUser




class VideoCasets(models.Model):
    name = models.CharField(max_length=70)
    price = models.FloatField()
    date_of_production = models.DateField(auto_created=True)
    length_of_film = models.TimeField()
    type = models.ForeignKey('Types',on_delete=models.CASCADE, blank=True,null=True)
    volume = models.FloatField()
    height = models.FloatField()
    length = models.FloatField()
    width = models.FloatField()
    image = models.ImageField(upload_to='media',null=True)
    genre = models.ForeignKey('Genre',on_delete=models.SET_NULL,null=True)
    class Meta:
        pass
    def __str__(self):
        return self.name

class Types(models.Model):
    name = models.CharField(max_length=70)
    def __str__(self):
        return self.name

LVL =(('Worker','worker'),
      ('Client','client'))

class User(AbstractUser):
    lvl = models.CharField(choices=LVL,default='worker',max_length=25)
    phone = models.CharField(max_length=20)
    pasport = models.CharField(max_length=20)
    date_of_birth = models.DateField(auto_now_add=True)
    cart = models.ManyToManyField(VideoCasets,related_name='cart')
    liked = models.ManyToManyField(VideoCasets,related_name='liked')

    def __str__(self):
        return self.username

class Genre(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


