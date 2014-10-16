from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web_interface.views.home', name='home'),
    url(r'^ldap/$','ldap_interface.views.index', name='ldap_test'),
    url(r'^courses$', 'web_interface.views.login', name='accepted'),
    url(r'^re-courses$', 'web_interface.views.reCaptchaLogin', name='reCaptcha'),
    url(r'^courses/[A-Z]{3}[0-9]{3}$','web_interface.views.viewAssessment', name='view_assessments_COSXXX'),
    url(r'^logout$', 'web_interface.views.logout', name='logout'),
   # url(r'courses/([A-Z]{3}[0-9]{3})/assessments/view$','web_interface.views.getAllAssessmentOfModule', name='view_assessment'),
   url(r'courses/([A-Z]{3}[0-9]{3})/assessments/view$','web_interface.views.getAllAssessmentOfModule', name='view_assessment'),
    url(r'^User$','web_interface.views.personDetails', name='person_details'),
    url(r'courses/[A-Z]{3}[0-9]{3}/[A-Za-z0-9 _]*[A-Za-z0-9][A-Za-z0-9 _]*/sessions$','web_interface.views.getAllSessionsForAssessment', name='view_sessions'),
    #url(r'create$','web_interface.views.createAssessment', name='create_assessment'),
    url(r'create-session$','web_interface.views.createSession', name='create_session'),
    url(r'view-students$','web_interface.views.getAllStudentOfModule', name='add_user_to_session'),
    url(r'update-info$','web_interface.views.addStudentToSession', name='added_user_to_session'),
    url(r'session-info$','web_interface.views.getAllPersonOfSession', name='view_user_in_session'),
    #url(r'[A-Za-z0-9 _]*[A-Za-z0-9][A-Za-z0-9 _]*$','web_interface.views.testingAssessment', name='view_children_assessment'),
    url(r'lecturer$','web_interface.views.getAllAssessmentOfAssessment', name='view_children_assessment'),
    url(r'create-leaf-assessment$','web_interface.views.createLeafAssessment', name='create_leaf_assessment'),
    url(r'update_mark$','web_interface.views.updateMarkForStudent', name='update_student_mark'),
    url(r'remove$','web_interface.views.deleteAssessment', name='delete_assessment'),
    url(r'remove-session$','web_interface.views.deleteSession', name='delete_session'),
    url(r'update-fullmark','web_interface.views.changeAssessmentFullMark', name='update_leaf_total_mark'),
    url(r'change-status','web_interface.views.openOrCloseSession', name='update_session_status'),
    url(r'^hamster_home','web_interface.views.backHome', name='hamster_home'),
    url(r'view-assessments$','web_interface.views.viewAssessmentForMarker', name='view_marker_assessment'),
    url(r'view_student_assessment$','web_interface.views.viewStudentsForAssessment', name='view_student_assessment'),
    url(r'^user-mode$','web_interface.views.use_as', name='use_as_redirect'),
    url(r'published','web_interface.views.setPublishedStatus', name='update_assessment_published'),
    url(r'^update_sub_assessment_published','web_interface.views.setPublishedStatusInLeaf', name='update_sub_assessment_published'),
    url(r'assessment_marking','web_interface.views.getLeafAssessmentPage', name='view_leaf'),
    
    url(r'view_marker_sessions$','web_interface.views.viewSessionForMarker', name='view_marker_sessions'),
    url(r'view_marker_assessment$','web_interface.views.viewAssessmentForMarker', name='view_marker_assessment'),
    url(r'view-student$','web_interface.views.viewStudentsForAssessment', name='view_students_of_assessemnts'),
    url(r'update-marks$','web_interface.views.updateMarkForStudentMarker', name='update_mark_marker'),
    
    url(r'view_student_assessment$','web_interface.views.viewAssessmentsForStudent', name='view_student_assessment'),
    url(r'student-assessment','web_interface.views.getAllChildrenOfAssessmentForStudent', name='view_children_assessment_student'),
    #url(r'testingAssess$','web_interface.views.testingStudentAssessmentForModule', name='view_children_assessment_student'),
    
    url(r'aggregateMarkForAssessment$','web_interface.views.aggregateMarkForAssessment', name='aggregateMarkForAssessment'),
    url(r'assessmentReport$','reporting.views.get_assessment_report', name='assessment_report'),
    url(r'print_pdf$','reporting.views.get_student_marks_pdf', name='generate_pdf_for_student'),
    url(r'print_csv$','reporting.views.get_student_marks_csv', name='generate_csv_for_student'),
    url(r'change-time$','web_interface.views.ChangeSessionTime', name='change-time'),
    url(r'remove-stud$','web_interface.views.removeUserfromSession', name='remove-stud'),
    url(r'audit_log$','web_interface.views.AuditLog', name='audit_log'),
    url(r'audit_add_module$','web_interface.views.addModule', name='audit_add_module'),
    url(r'added-student','web_interface.views.addStudentToModule', name='added-student'),
    url(r'added-lecture','web_interface.views.addLectureToModule', name='added-lecture'),
    url(r'added-tutor','web_interface.views.addTutorToModule', name='added-tutor'),
    url(r'student-removed','web_interface.views.removeStudentFromModule', name='student-removed'),
    url(r'lecture-removed','web_interface.views.removeLectureFromModule', name='added-lecture'),
    url(r'tutor-removed','web_interface.views.removeTutorFromModule', name='tutor-removed'),
    
    url(r'importCSV$','reporting.views.import_csv', name='import_csv'),
    # Assessment Centre
    url(r'aggregate$','web_interface.views.assessmentCenter', name='assessment_center'),
    url(r'assessmentCenterLeaf$','web_interface.views.assessmentCenterLeaf', name='assessment_center_leaf'),
    
    url(r'update-name','web_interface.views.changeAssessmentName', name='update_assessment_name'),
    
    url(r'^admin/', include(admin.site.urls)),
)
