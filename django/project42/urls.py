from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^project42/', include('project42.foo.urls')),
    (r'^$', 'project42.mobile.views.index'),
    (r'^jennielees', 'project42.mobile.views.demo'),
    (r'^chiprodgers', 'project42.mobile.views.demo2'),
    (r'^(?P<twittername>\w+)', 'project42.mobile.views.recommendations')

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
