# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

from django.utils.safestring import mark_safe

from django.core.urlresolvers import reverse

class Album(models.Model):
    '''
        Model to store images in a group and give them a name.
        Owner is safed, to enable controlled editing.
    '''
    name = models.CharField(max_length=40)
    images = models.ManyToManyField("Image", blank=True)
    is_public = models.BooleanField(default=False)
    owner = models.ForeignKey(User)
    category = models.ForeignKey("AlbumCategory", blank=True, null=True)
    ordering = models.IntegerField()

    @models.permalink
    def get_absolute_url(self):
        return ('comenius:album-detail', (), {'pk':self.pk})

    class Meta:
        ordering = ['ordering']

class Image(models.Model):
    '''
        Safe images with a description
    '''
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    description = models.CharField(max_length=255, blank=True)
    public = models.BooleanField(default=True)

    def __unicode__(self):
        return mark_safe(u"%s: <img src=\"%s\" style=\"height:100px;\">" % (self.description, self.image.url))

class School(models.Model):
    '''
        Safe school to connect students to them
    '''
    name = models.CharField(max_length=120)
    homepage = models.URLField()
    location = models.TextField()
    students = models.ManyToManyField(User)
    
    def __unicode__(self):
        return self.name


class Project(models.Model):
    '''
        Publish projects on website
    '''
    slug = models.SlugField(primary_key=True)
    title = models.CharField(max_length=140)
    short_desc = models.TextField()
    description = models.TextField()
    album = models.ForeignKey(Album)
    users = models.ManyToManyField(User)
    school = models.ForeignKey(School)
    category = models.ForeignKey("Category")
    documents = models.ForeignKey("Document", blank=True, null=True)
    pdf = models.FileField(upload_to="documents/pdf/", blank=True, null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('comenius:project-detail', (), {'slug':self.slug})

    class Meta:
        ordering = ['title']
class Category(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.TextField()
    
    def __unicode__(self):
        return self.name

class Document(models.Model):
    document = models.FileField(upload_to="documents/%Y/%m/%d")
    name = models.CharField(max_length=80)
    owner = models.ForeignKey(User)


class Event(models.Model):
    date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=140)
    description = models.TextField()
    owner = models.ForeignKey(User)
    @models.permalink
    def get_absolute_url(self):
        return ('comenius:index', (), {})

class Report(models.Model):
    title = models.CharField(max_length=140)
    content = models.TextField()
    owner = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.title

class Mobility(models.Model):
    name = models.CharField(max_length=140)
    reports = models.ManyToManyField(Report)
    ordering = models.IntegerField()

    class Meta:
        ordering = ['ordering']


class AlbumCategory(models.Model):
    name = models.CharField(max_length=140)
    ordering = models.IntegerField()
    image = models.ImageField(upload_to="logos/",blank=True, null=True)

    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ["ordering"]

