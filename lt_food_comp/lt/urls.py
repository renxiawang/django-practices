from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lt.views.home', name='home'),
    # url(r'^lt/', include('lt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # static files
    url(r'css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'D:/webweb/linxiaoyan/lt/lt_food/templates/css'}),
    url(r'js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'D:/webweb/linxiaoyan/lt/lt_food/templates/js'}),
    url(r'img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'D:/webweb/linxiaoyan/lt/lt_food/templates/img'}),
    url(r'product-imgs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'D:/webweb/linxiaoyan/lt/lt_food/product-imgs'}),

    url(r'^index/$', 'lt_food.views.index'),
    url(r'^admin$', 'lt_food.views.login'),
    url(r'^admin/login$', 'lt_food.views.verify_admin'),
    url(r'^admin/logout$', 'lt_food.views.logout'),
    url(r'^admin/del-news/(?P<news_id>\d*)$', 'lt_food.views.del_news'),
    url(r'^admin/del-product/(?P<product_id>\d*)$', 'lt_food.views.del_product'),
    url(r'^admin/(?P<selected>.*)$', 'lt_food.views.admin'),
    url(r'^about/(?P<selected>.*)$', 'lt_food.views.about'),
    url(r'^products/(?P<selected>.*)$', 'lt_food.views.products'),
    url(r'^contact/$', 'lt_food.views.contact'),
    url(r'^news/(?P<news_id>\d+)/$', 'lt_food.views.news'),
    
    url(r'', 'lt_food.views.index'),
    
    
)
