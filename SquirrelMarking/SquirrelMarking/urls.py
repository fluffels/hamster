from django.conf.urls import patterns, include, url
from SquirrelMarking.views import *

urlpatterns = patterns('',
	(r'^$', login),
	(r'^student/$', student_home),
	(r'^lecturer/$', lecturer_home),
	(r'^marker/$', marker_home),
	(r'^assessmentView/$', assessment_view),
	(r'^assessmentManager/$', assessment_manager),
	(r'^sessionManager/$', session_manager),
	
	(r'^auditReport/$', audit_report),
	(r'^Reporting_Main/$', reporting_main),
	(r'^Statistics/$', statistics),
	(r'^studentChosen/$', student_chosen),
	(r'^studentReport/$', student_report),
	(r'^unpublish/$', unpublish),
	(r'^marks-management/$', marks_management),
        (r'^checkLogin/$', user_login),
        (r'^test/$', test),
)
