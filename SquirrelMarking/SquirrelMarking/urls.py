from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
	#home page
	(r'^$', loginWeb),
	(r'^getAssessments/$', viewAssessments),
	#student report page
	#~ (r'^studentReport/$', studentReport),
	#~ #audit report page
	#~ (r'^auditReport/$', auditReport),
	#~ #marker home page
	#~ (r'^marker/$', marker_home),
	#assessments view
	(r'^assessmentView/$', assessment_view),
	#manage assessments
	(r'^assessmentManager/$', assessment_manager),
	#manage sessions
	(r'^sessionManager/$', session_manager),
	#view audit report
	(r'^auditReport/$', view_audit_report),
	#reporting mani menu
	(r'^Reporting_Main/$', reporting_main),
	#statistics
	(r'^Statistics/$', statistics),
	#all students
	(r'^students/$', view_all_students),
	#view individual student
	(r'^student/(?P<studentNumber>\w{1}\d{8})/$', view_student),
	(r'^studentReport/$', student_report),
	(r'^unpublish/$', unpublish),
	(r'^marks-management/$', marks_management),
	#view individual course
	(r'^course/(?P<courseCode>\w{3}\d{3})/$', view_course),
	#view all courses
	(r'^courses/$', view_all_course),
	
	(r'^auditReport/$', audit_report),
	(r'^Reporting_Main/$', reporting_main),
	(r'^Statistics/$', statistics),
	#(r'^studentChosen/$', student_chosen),
	#(r'^studentReport/$', student_report),
	(r'^unpublish/$', unpublish),
	(r'^marks-management/$', marks_management),
	(r'frequency_analysis/$', frequency_analysis),
	#(r'get_module_mark/$', get_module_mark),
	(r'getAssessments/$', getAssessments),
	(r'getLeafAssessments/$', getLeafAssessments),
	(r'getLecturerModules/$', getLecturerModules),
	(r'studentModules/$', studentModules),
	(r'searchStudents/$', searchStudents),
	(r'displayStudent/$', displayStudent),
)