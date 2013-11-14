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
# Create your views here.

site = []


site.append(nav("Home", reverse('comenius:index')))

"""site.append(nav("Search", reverse('comenius:search', (), {})))"""

projekte = []

for category in Category.objects.all():
    projekte.append(nav(category.name, reverse('comenius:category-detail', kwargs={'slug':category.slug})))

site.append(nav("Projekte", subsites=projekte))

site.append(nav("Galerie", reverse('comenius:album-list')))

extra = {
    "site": site,
    "appname": "Comenius Projekt",
    "homeurl": reverse('comenius:index'),
    "events": Event.objects.all()[:5],
}

app_specific['comenius'] = extra

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

login = lambda request: django.contrib.auth.views.login(request, extra_context=dict(extra.items() + {'title':"Login"}.items()))

logout = lambda request: django.contrib.auth.views.logout(request, extra_context=dict(extra.items()))

search = ExtraTemplateView.as_view(
        template_name="comenius/search.html",
        extra={
            'title': "Suche",
            'appname': 'comenius',
        })

class CreateOwnerView(ExtraCreateView):

    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateOwnerView, self).form_valid(form)

album_create = login_required(
	CreateOwnerView.as_view(
	    model = Album,
        fields = ['name', 'is_public'],
        extra = {
            'title': "Album erstellen",
            'appname': 'comenius',
        })
)

album_detail = ExtraDetailView.as_view(
        model = Album,
        extra = {
            'title': lambda c: c['object'].name,
            'appname': "comenius",
        })
        
class AlbumListView(ExtraListView):
    def get_queryset(self):
        if(self.request.user.is_authenticated()):
            return Album.objects.all()
        else:
            return Album.objects.filter(is_public=True)

album_list = AlbumListView.as_view(
        extra = {
            'title': "Fotos",
            'appname': "comenius",
        }
)

category_detail = ExtraDetailView.as_view(
        model = Category,
        extra = {
            'title': "Projekte",
            'categories': Category.objects.all(),
            'appname': "comenius"
        }
)

report_detail = ExtraDetailView.as_view(
        model = Report,
        extra = {
            'title': lambda c: c['object'].title,
            'appname': "comenius",
        }
)


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

class ImageCreateView(ExtraCreateView):
    def form_valid(self, form):
        self.object = form.save()
        album = Album.objects.get(pk=1)
        album.images.add(self.object)
        album.save()
        self.success_url = reverse('comenius:album-detail', kwargs={'pk': album.pk})
        return super(ImageCreateView, self).form_valid(form)

image_album_add = login_required(
        ImageCreateView.as_view(
            model = Image,
            fields = ["description", "image"],
        )
)

class ProjectCreateView(ExtraCreateView):
    def form_valid(self, form):
        form.instance.album = Album.objects.create(name=form.instance.title, is_public=True, owner=self.request.user)
        return super(ProjectCreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('comenius:project-detail', kwargs={'slug': self.object.slug})

project_create = ProjectCreateView.as_view(
        model = Project,
        fields = ["title", "slug", "short_desc", "description", "users", "school", "category"],
        
        
        extra = {
            'title': "Projekt hochladen",
            'categories': Category.objects.all(),
            'appname': "comenius",
        }
)

project_detail = ExtraDetailView.as_view(
        model = Project,
        extra = {
            'title': lambda c: c['object'].title,
            'categories': Category.objects.all(),
            'appname': "comenius",
        }
        
)

