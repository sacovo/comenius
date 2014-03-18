# coding=utf-8
import os

from djangoutils.views.generic import *
from djangoutils import NavigationPoint as nav

import django.contrib.auth.views

from django.conf import settings

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy as reverse
from django.core.urlresolvers import reverse as reverse_
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test

from comenius.models import Album, Category, Report, Event, Image, Project

site = []

projects = []

order = ["Umwelt", "Verkehr", u"Ern\xe4hrung", "Energie"]

for category in Category.objects.all():
    projects.append(nav(category.name,
        reverse('comenius:category-detail', kwargs={'slug':category.slug})))

key=lambda d:order.index(d.name)

projects.sort(key=key)

site.append(nav("Projekte", subsites=projects))

site.append(nav("Galerie", reverse('comenius:album-list')))

extra = {
    "site": site,
    "appname": "Comesco Nachhaltigkeit",
    "homeurl": reverse('comenius:index'),
    "events": lambda one: Event.objects.all()[:5],
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
        post = self.request.POST
        album = Album.objects.get(pk=self.request.POST['album'])
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

class SpecialUpdateView(ExtraUpdateView):
    test_func = None

    def get_object(self, queryset=None):
        obj = super(SpecialUpdateView, self).get_object(queryset)
        if(self.test_func(self.request.user, obj)):
            return obj
        raise PermissionDenied


class SpecialDeleteView(ExtraDeleteView):
    test_func = None

    def get_object(self, queryset=None):
        obj = super(SpecialDeleteView, self).get_object(queryset)
        if(self.test_func(self.request.user, obj)):
            return obj
        raise PermissionDenied

#-------------------------------------------------------------------------------
# Special Views: index, impressum, about, login, logout, search
#-------------------------------------------------------------------------------

image_dir = os.path.join(settings.STATIC_ROOT, 'comenius/imgs/headers/')

images = os.listdir(image_dir)

titles = []

subtitels = []

map_func = lambda image, title, subtitle: (image, title or "", subtitle or "")

images = map(map_func, images, titles, subtitels)

index = ExtraTemplateView.as_view(
                template_name="comenius/index.html",
                extra={
                    'title': "Home",
                    'appname': "comenius",
                    'images': images,
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

password_change = lambda request: django.contrib.auth.views.password_change(request,
                post_change_redirect=reverse('comenius:password-change-done'),
                extra_context=dict(extra.items() + {'title': "Passwort"}.items()))

password_change_done = lambda request: django.contrib.auth.views.password_change_done(request,
                extra_context=dict(extra.items() + {'title': "Passwort"}.items()))


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


album_create_view = CreateOwnerView.as_view(
	model = Album,
        fields = ['name', 'is_public'],
        extra = {
            'title': "Album erstellen",
            'appname': 'comenius',
        }
)

def album_create(request, *args, **kwargs):
    if(request.user.has_perms(['comenius.can_add_album'])):
        return album_create_view(request, *args, **kwargs)
    else:
        raise PermissionDenied()


album_update = SpecialUpdateView.as_view(
        test_func = lambda user, obj: user == obj.owner,
        model = Album,
        fields = ['name', 'is_public'],
        extra = {
            'title': lambda c: c['object'].name,
            'appname': "comenius",
        }
)

album_delete = SpecialDeleteView.as_view(
        test_func = lambda user, obj: user == obj.owner,
        model = Album,
        success_url = reverse('comenius:album-list'),
        extra = {
            'title': lambda c: c['object'].name,
            'appname': "comenius",
        }
)


key2 = lambda d: order.index(d.name)
# Category

category_list = ExtraListView.as_view(
        model = Category,
        extra = {
            'title': "Projekte",
            'categories': sorted(Category.objects.all(),key=key2),
            'appname': "comenius",
        }
)


category_detail = ExtraDetailView.as_view(
        model = Category,
        extra = {
            'title': "Projekte",
            'categories': sorted(Category.objects.all(),key=key2),
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

project_create = login_required(
    ProjectCreateView.as_view(
        model = Project,
        fields = ["title", "slug", "short_desc", "description",
                    "school", "users", "category"],

        extra = {
            'title': "Projekt hochladen",
            'categories': Category.objects.all(),
            'appname': "comenius",
        }
    )
)

project_update = SpecialUpdateView.as_view(
        test_func = lambda user, obj: user in obj.users.all(),
        model = Project,
        fields = ["title", "slug", "short_desc", "description",
                    "school", "users", "category"],
        
        extra = {
            'title': lambda c: c['object'].title,
            'categories': Category.objects.all(),
            'appname': "comenius",
        }
)

project_delete = SpecialDeleteView.as_view(
        test_func = lambda user, obj: user in obj.users.all(),
        model = Project,
        success_url = reverse('comenius:index'),
        extra = {
            'title': lambda c: c['object'].title(),
            'categories': Category.objects.all(),
            'appname': "comenius",
        }
)
