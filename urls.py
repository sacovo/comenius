from django.conf.urls import patterns, url, include

from djangoutils.views.generic import app_specific
from comenius.models import Category

urlpatterns = patterns('comenius.views',
    url(r"^$", 'index', name="index"),
    url(r"^accounts/login/$", 'login', name="login", ),
    url(r"^accounts/logout/$", 'logout', name="logout"),
    url(r"^accounts/password-change/$", 'password_change', name="password-change"),
    url(r"^accounts/password-change-done/$", 'password_change_done', name="password-change-done"),
    url(r"^album/add-image/", 'image_album_add', name="image-album-add"),
    url(r"^album/$", 'album_list', name="album-list"),
    url(r"^album/create/$", 'album_create', name="album-create"),
    url(r"^album/(?P<pk>[\d]+)/$", 'album_detail', name="album-detail"),
    url(r"^album/(?P<pk>[\d]+)/update/$", 'album_update', name="album-update"),
    url(r"^album/(?P<pk>[\d]+)/delete/$", 'album_delete', name="album-delete"),
    url(r"^categories/(?P<slug>[\w-]+)/$", 'category_detail', name="category-detail"),
    url(r"^categories/$", 'category_list', name="category-list"),
    url(r"^event/create/$", 'event_create', name="event-create"),
    url(r"^event/(?P<pk>[\d]+)/update/'$", 'event_update', name="event-update"),
    url(r"^impressum/$", 'impressum', name="impressum"),
    url(r"^project/create/$", 'project_create', name="project-create"),
    url(r"^project/(?P<slug>[\w-]+)/$", 'project_detail', name="project-detail"),
    url(r"^project/(?P<slug>[\w-]+)/update/$", 'project_update', name="project-update"),
    url(r"^project/(?P<slug>[\w-]+)/delete/$", 'project_delete', name="project-delete"),
    url(r"^reports/(?P<pk>[\d]+)/$", 'report_detail', name="report-detail"),
    url(r"^search/$", 'search', name="search"),
    url(r"^mobility/(?P<pk>[\d]+)/$", 'mobility_detail', name="mobility-detail"),
    url(r"^categories/$", 'albumcategory_list', name="album-category-list"),
)
