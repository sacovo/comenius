from django.db import models
from django.contrib.auth.models import User

class Album(models.Model):
    name = models.CharField(max_length=40)
    images = models.ManyToManyField("Image")
    owner = models.ForeignKey(User)

class Image(models.Model):
    pass
