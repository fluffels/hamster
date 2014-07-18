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
    url(r'^create_session$','web_interface.views.createSession', name='create_session'),
    url(r'^add_user_to_session$','web_interface.views.getAllStudentOfModule', name='add_user_to_session'),
    url(r'^added_user_to_session$','web_interface.views.addStudentToSession', name='added_user_to_session'),
    url(r'^view_user_in_session$','web_interface.views.getAllPersonOfSession', name='view_user_in_session'),
    url(r'^view_children_assessment$','web_interface.views.getAllChildrenOfAssessment', name='view_children_assessment'),
    url(r'^create_leaf_assessment$','web_interface.views.createLeafAssessment', name='create_leaf_assessment'),
    url(r'^update_mark$','web_interface.views.updateMarkForStudent', name='update_student_mark'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
