from django.conf.urls import patterns, url, include

from djangoutils.views.generic import app_specific

urlpatterns = patterns('comenius.views',
    url(r"^$", 'index', name="index"),
    url(r"^impressum/$", 'impressum', name="impressum"),
    url(r"^accounts/login/$", 'login', name="login", ),
)

'''
urlpatterns += patterns('django.contrib.auth.views',
    url(r"^accounts/login/$", 'login', name="login", ),
)
'''
