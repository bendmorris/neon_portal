from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sp_list.views',
    url(r'^upload/', 'upload', name='upload'),
    url(r'^enter/', 'enter', name='enter'),
    url(r'^jobs/', 'jobs', name='jobs'),
    url(r'^list/(?P<taxon>[a-zA-Z]+)/(?P<site>[a-zA-Z]+)/', 'download_csv', name='download_csv'),
    url(r'^list/', 'list', name='list'),
    url(r'^delete/(?P<id>\d{1,4})/$', 'delete', name='delete'),
    url(r'^kill/(?P<id>\d{1,4})/$', 'kill', name='kill'),
    url(r'^process/', 'process', name='process'),
)
