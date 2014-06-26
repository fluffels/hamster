from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'web_interface.views.home', name='home'),
     url(r'^ldap/$','ldap_interface.views.index', name='ldap_test'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
