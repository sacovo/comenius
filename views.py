# Create your views here.

from djangoutils.views.generic import *
from djangoutils import NavigationPoint as nav
import django.contrib.auth.views
from django.core.urlresolvers import reverse_lazy as reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from comenius.models import Album
# Create your views here.

site = []

site.append(nav("Home", reverse('comenius:index')))
site.append(nav("Impressum", reverse('comenius:impressum')))

album_nav = [
    nav("Album Erstellen", reverse('comenius:album-create')),
]

site.append(nav("Album", subsites=album_nav))

blog_extra = {
    "site": site,
    "appname": "Comenius Projekt",
    "homeurl": reverse('comenius:index'),
}

app_specific['comenius'] = blog_extra

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

login = lambda request: django.contrib.auth.views.login(request, extra_context=dict(blog_extra.items() + {'title':"Login"}.items()))

logout = lambda request: django.contrib.auth.views.logout(request, extra_context=dict(blog_extra.items()))

search = ExtraTemplateView.as_view(
        template_name="comenius/search.html",
        extra={
            'title': "Suche",
            'appname': 'comenius',
        })

class AlbumCreate(ExtraCreateView):
    model = Album
    fields = ['name']
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AlbumCreate, self).form_valid(form)

@login_required
album_create = AlbumCreate.as_view(
        extra = {
            'title': "Album erstellen",
            'appname': 'comenius',
        })
