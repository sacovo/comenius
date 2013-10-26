from django.conf.urls import patterns, url, include

urlpatterns = patterns('comenius.views',
    url(r"^$", 'index', name="index"),
)
