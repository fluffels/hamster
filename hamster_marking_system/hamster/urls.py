from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web_interface.views.home', name='home'),
    url(r'^ldap/$','ldap_interface.views.index', name='ldap_test'),
    url(r'^success$', 'web_interface.views.login', name='accepted'),
    url(r'^$', 'web_interface.views.logout', name='logout'),
    url(r'^view_assessment$','web_interface.views.getAllAssessmentOfModule', name='view_assessment'),
    url(r'^person_details$','web_interface.views.personDetails', name='person_details'),
    url(r'^view_session$','web_interface.views.getAllSessionsForAssessment', name='view_sessions'),
    url(r'^create_assessment$','web_interface.views.createAssessment', name='create_assessment'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
