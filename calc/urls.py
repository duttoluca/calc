from django.conf.urls import patterns, url

from accert.views import calcolaAccert

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'calc.views.home', name='home'),
    # url(r'^calc/', include('calc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^accert/$', calcolaAccert, name='calcolaAccert'),
)
