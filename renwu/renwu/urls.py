from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'renwu.views.home', name='home'),
    # url(r'^renwu/', include('renwu.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/workspace/fyp/renwu/search_engine/templates/css'}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/workspace/fyp/renwu/search_engine/templates/js'}),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/workspace/fyp/renwu/search_engine/templates/img'}),

    url(r'^$', 'search_engine.views.index'),
    url(r'^search$', 'search_engine.views.list_search_results'),
    url(r'^person/(?P<pid>.*)$', 'search_engine.views.display_personal_details')
)
