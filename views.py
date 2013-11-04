# Create your views here.

from djangoutils.views.generic import *
from djangoutils import NavigationPoint as nav

from django.core.urlresolvers import reverse_lazy as reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

# Create your views here.

site = []

site.append(nav("Home", reverse('comenius:index')))
site.append(nav("Impressum", reverse('comenius:impressum')))

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
		