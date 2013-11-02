from django.conf.urls import patterns, url, include

urlpatterns = patterns('comenius.views',
    url(r"^$", 'index', name="index"),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r"^accounts/login/$", 'login', name="login"),
)
