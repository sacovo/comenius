from django.contrib.admin import site
from models import Category, School, Event, Report, Image, Album, Mobility, AlbumCategory

site.register((Category, School, Event, Report, Image, Album, Mobility, AlbumCategory))
