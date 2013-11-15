# Create your views here.

from djangoutils.views.generic import *
from djangoutils import NavigationPoint as nav

import django.contrib.auth.views

from django.core.urlresolvers import reverse_lazy as reverse
from django.core.urlresolvers import reverse as reverse_
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from comenius.models import Album, Category, Report, Event, Image, Project

site = []

site.append(nav("Home", reverse('comenius:index')))

projects = []

for category in Category.objects.all():
    projects.append(nav(category.name,
        reverse('comenius:category-detail', kwargs={'slug':category.slug})))

site.append(nav("Projekte", subsites=projects))

site.append(nav("Galerie", reverse('comenius:album-list')))

extra = {
    "site": site,
    "appname": "Comenius Projekt",
    "homeurl": reverse('comenius:index'),
    "events": Event.objects.all()[:5],
}

app_specific['comenius'] = extra

class CreateOwnerView(ExtraCreateView):
    '''
        Create View that adds an owner field based on request.user to the object
    '''
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateOwnerView, self).form_valid(form)


class AlbumListView(ExtraListView):
    '''
        List view that displays only public albums if one is not loggged in
    '''
    def get_queryset(self):
        if(self.request.user.is_authenticated()):
            return Album.objects.all()
        else:
            return Album.objects.filter(is_public=True)


class ImageCreateView(ExtraCreateView):
    '''
        Create view for images. Adds the image to a given album
    '''
    def form_valid(self, form):
        self.object = form.save()
        album = Album.objects.get(pk=1)
        album.images.add(self.object)
        album.save()
        self.success_url = reverse('comenius:album-detail', kwargs={'pk': album.pk})
        return super(ImageCreateView, self).form_valid(form)


class ProjectCreateView(ExtraCreateView):
    def form_valid(self, form):
        '''
            Append an album to every project that is created
        '''
        form.instance.album = Album.objects.create(name=form.instance.title,
                                    is_public=True, owner=self.request.user)
        return super(ProjectCreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('comenius:project-detail',
                    kwargs={'slug': self.object.slug})

#-------------------------------------------------------------------------------
# Special Views: index, impressum, about, login, logout, search
#-------------------------------------------------------------------------------

index = ExtraTemplateView.as_view(
                template_name="comenius/index.html",
                extra={
                    'title': "Home",
                    'appname': "comenius",
                })

impressum = ExtraTemplateView.as_view(
                template_name="comenius/impressum.html",
                extra={
                    'title': "Impressum",
                    'appname': "comenius",
                })

about = ExtraTemplateView.as_view(
		template_name="comenius/about.html",
		extra={
		    'title': "About",
		    'appname': "comenius",
		})

login = lambda request: django.contrib.auth.views.login(request,
                extra_context=dict(extra.items() + {'title':"Login"}.items()))

logout = lambda request: django.contrib.auth.views.logout(request,
                                            extra_context=dict(extra.items()))

search = ExtraTemplateView.as_view(
        template_name="comenius/search.html",
        extra={
            'title': "Suche",
            'appname': 'comenius',
        })

#-------------------------------------------------------------------------------
# Generic views for database models
#-------------------------------------------------------------------------------

# Album

album_list = AlbumListView.as_view(
        extra = {
            'title': "Fotos",
            'appname': "comenius",
        }
)


album_detail = ExtraDetailView.as_view(
        model = Album,
        extra = {
            'title': lambda c: c['object'].name,
            'appname': "comenius",
        }
)


album_create = login_required(
	CreateOwnerView.as_view(
	    model = Album,
        fields = ['name', 'is_public'],
        extra = {
            'title': "Album erstellen",
            'appname': 'comenius',
        })
)

# Category

category_detail = ExtraDetailView.as_view(
        model = Category,
        extra = {
            'title': "Projekte",
            'categories': Category.objects.all(),
            'appname': "comenius"
        }
)

# Report

report_detail = ExtraDetailView.as_view(
        model = Report,
        extra = {
            'title': lambda c: c['object'].title,
            'appname': "comenius",
        }
)

# Event

event_create = login_required(
        CreateOwnerView.as_view(
            model = Event,
            fields = ["name", "date", "description"],
            extra = {
                'title': "Termin eintragen",
                'appname': "comenius",
            }
    )
)


event_update = login_required(
        ExtraUpdateView.as_view(
            model = Event,
            fields = ["name", "date", "description"],
            extra = {
                'title': "Termin bearbeiten",
                'appname': "comenius",
            }
        )
)

# Image

image_album_add = login_required(
        ImageCreateView.as_view(
            model = Image,
            fields = ["description", "image"],
        )
)

# Project

project_detail = ExtraDetailView.as_view(
        model = Project,
        extra = {
            'title': lambda c: c['object'].title,
            'categories': Category.objects.all(),
            'appname': "comenius",
        }
        
)

project_create = ProjectCreateView.as_view(
        model = Project,
        fields = ["title", "slug", "short_desc", "description",
                "users", "school", "category"],

        extra = {
            'title': "Projekt hochladen",
            'categories': Category.objects.all(),
            'appname': "comenius",
        }
)

