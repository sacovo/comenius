from django.conf.urls import patterns, url, include

from djangoutils.views.generic import app_specific

urlpatterns = patterns('comenius.views',
    url(r"^$", 'index', name="index"),
    url(r"^impressum/$", 'impressum', name="impressum"),
    url(r"^search/$", 'search', name="search"),
    url(r"^accounts/login/$", 'login', name="login", ),
    url(r"^accounts/logout/$", 'logout', name="logout"),
    url(r"^album/create/$", 'album_create', name="album-create"),
    url(r"^album/(?P<pk>\d+)/$", 'album_detail', name="album-detail")
)
