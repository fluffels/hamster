from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Examples:
     url(r'^success/$', 'web_interface.views.login', name='accepted'),
     url(r'^logout$', 'web_interface.views.logout', name='logout'),
)