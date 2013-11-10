from django.db import models
from django.contrib.auth.models import User

class Album(models.Model):
    name = models.CharField(max_length=40)
    images = models.ManyToManyField("Image", blank=True)
    owner = models.ForeignKey(User)
    


class Image(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m%/%d")
    description = models.CharField(max_length=255, blank=True)

