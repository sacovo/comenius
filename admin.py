from django.contrib.admin import site
from models import Category, School, Event, Report, Image, Album

site.register((Category, School, Event, Report, Image, Album))
