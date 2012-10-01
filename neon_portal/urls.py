from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('sp_list.urls')),
    #url(r'^list/', include('neon_portal.sp_list_gen.urls')),

    # Examples:
    # url(r'^$', 'neon_portal.views.home', name='home'),
    # url(r'^neon_portal/', include('neon_portal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^content/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/ben/Dropbox/Dev/neon_portal/content'}),
    url(r'^', include('home.urls')),
)
