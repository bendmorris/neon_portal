from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
                       url(r'^logout', 'home.views.logout', name='logout'),
                       url(r'^', 'home.views.index', name='index'),
                       )
