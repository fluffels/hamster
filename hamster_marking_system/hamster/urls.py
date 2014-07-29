from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web_interface.views.home', name='home'),
    url(r'^ldap/$','ldap_interface.views.index', name='ldap_test'),
    url(r'^courses$', 'web_interface.views.login', name='accepted'),
    url(r'^course/([A-Z]{3}[0-9]{3})/$','web_interface.views.viewAssessment', name='view_assessments_COSXXX'),
    url(r'^$', 'web_interface.views.logout', name='logout'),
    url(r'courses/([A-Z]{3}[0-9]{3})/Assessments/$','web_interface.views.getAllAssessmentOfModule', name='view_assessment'),
    url(r'^User$','web_interface.views.personDetails', name='person_details'),
    url(r'^courses/([A-Z]{3}[0-9]{3})/([aA-zZ]{1,})/sessions$','web_interface.views.getAllSessionsForAssessment', name='view_sessions'),
    url(r'create$','web_interface.views.createAssessment', name='create_assessment'),
    url(r'session/create$','web_interface.views.createSession', name='create_session'),
    url(r'^add_user_to_session$','web_interface.views.getAllStudentOfModule', name='add_user_to_session'),
    url(r'^added_user_to_session$','web_interface.views.addStudentToSession', name='added_user_to_session'),
    url(r'^view_user_in_session$','web_interface.views.getAllPersonOfSession', name='view_user_in_session'),
    url(r'^view_children_assessment$','web_interface.views.getAllChildrenOfAssessment', name='view_children_assessment'),
    url(r'^create_leaf_assessment$','web_interface.views.createLeafAssessment', name='create_leaf_assessment'),
    url(r'^update_mark$','web_interface.views.updateMarkForStudent', name='update_student_mark'),
    url(r'remove$','web_interface.views.deleteAssessment', name='delete_assessment'),
    url(r'^remove_session','web_interface.views.deleteSession', name='delete_session'),
    url(r'^update_leaf_total_mark','web_interface.views.changeAssessmentFullMark', name='update_leaf_total_mark'),
    url(r'^update_session_status','web_interface.views.openOrCloseSession', name='update_session_status'),
    url(r'^hamster_home','web_interface.views.backHome', name='hamster_home'),
    url(r'view_marker_assessment$','web_interface.views.viewAssessmentForMarker', name='view_marker_assessment'),
    url(r'view_student_assessment$','web_interface.views.viewStudentsForAssessment', name='view_student_assessment'),
    url(r'^use_as/([aA-zZ]{1,})/$','web_interface.views.use_as', name='use_as_redirect'),
    url(r'published','web_interface.views.setPublishedStatus', name='update_assessment_published'),
    url(r'^update_sub_assessment_published','web_interface.views.setPublishedStatusInLeaf', name='update_sub_assessment_published'),
    
    url(r'view_marker_sessions$','web_interface.views.viewSessionForMarker', name='view_marker_sessions'),
    url(r'view_marker_assessment$','web_interface.views.viewAssessmentForMarker', name='view_marker_assessment'),
    url(r'view_students_of_assessemnts$','web_interface.views.viewStudentsForAssessment', name='view_students_of_assessemnts'),
    url(r'update_mark_marker$','web_interface.views.updateMarkForStudentMarker', name='update_mark_marker'),
    
    url(r'view_student_assessment$','web_interface.views.viewAssessmentForStudent', name='view_student_assessment'),
    url(r'view_children_assessment_student$','web_interface.views.getAllChildrenOfAssessmentForStudent', name='view_children_assessment_student'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
