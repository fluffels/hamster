from django.conf.urls import patterns, include, url
from views import *
from Android import userUrls, studentUrls, markerUrls
import sys

import csv

urlpatterns = patterns('',
	#home page
	(r'^logout/$', logoutWeb),
	(r'^$', loginWeb),
	(r'^index/$', loginWeb),
	(r'^getCourseAssessments/$', getCourseAssessments),
	(r'^getAssessmentsOptions/$', viewAssessmentsOptions),
	(r'^getAssessmentSessionsOptions/$', viewAssessmentSessionsOptions),
	(r'^getSessionStudentMarks/$', getSessionStudentMarks),
	(r'^getAssessmentStudentMarks/$', getAssessmentStudentMarks),
	(r'^getLeafAssessmentStudentMarks/$', getLeafAssessmentStudentMarks),
	
	(r'^getLeafAssessmentsTableWeb/$', getLeafAssessmentsTableWeb),
	(r'^student/(?P<course>\w{6})/(?P<assessment>[0-9]+)/$', studentPage),
	(r'^tutor/(?P<course>\w{6})/(?P<assessment>[0-9]+)/$', tutorPage),
	(r'^teachingAssistant/(?P<course>\w{6})/(?P<assessment>[0-9]+)/$', teachingAssistantPage),
	(r'^lecturer/(?P<course>\w{6})/(?P<assessment>[0-9]+)/$', lecturerPage),
	
	(r'^tutor/(?P<course>\w{6})/(?P<assessment>[0-9]+)/(?P<session>[0-9]+)/$', tutorPage),
	(r'^teachingAssistant/(?P<course>\w{6})/(?P<assessment>[0-9]+)/(?P<session>[0-9]+)/$', teachingAssistantPage),
	(r'^lecturer/(?P<course>\w{6})/(?P<assessment>[0-9]+)/(?P<session>[0-9]+)/$', lecturerPage),
	(r'^marks-management/$', marks_management),
	
	(r'^lecturer/manage/$', manageCourse),
	(r'^lecturer/manage/(?P<course>\w{6})/$', manageCourse),
	(r'^lecturer/manage/(?P<course>\w{6})/(?P<assessmentID>[0-9]+)/$', manageCourseAssessment),
	(r'^updateAssessmentInformation/$', updateAssessmentInformation),
	#WEB PUBLISHING
	(r'^publish/$', publish),
	
	#WEB REPORTING
	(r'^auditReport/$', audit_report),
	(r'^studentReport/$', student_report),
	(r'^assessmentReport/$', assessment_report),
	(r'^saveAsPDF/$', save_as_pdf),
	(r'^saveAsCSV/$', save_as_csv),
	(r'^saveAsPDFStudent/$', save_as_pdf_student),
	(r'^saveAsCSVStudent/$', save_as_csv_student),
	(r'^saveAsPDFAssessment/$', save_as_pdf_assessment),
	(r'^saveAsCSVAssessment/$', save_as_csv_assessment),
	(r'^studentReportLeafAssessments/$', student_report_leaf_assessments),
	(r'^assessmentReportLeafAssessments/$', assessment_report_leaf_assessments),
	
	(r'^assessmentView/$', assessment_view),
	(r'^test/$', test),
	
	url(r'^Android/User/',include(userUrls)),
	url(r'^Android/Student/',include(studentUrls)),
	url(r'^Android/Marker/',include(markerUrls)),
	(r'^ldapTest/$', ldapTest),
	(r'^importTest/$', importTest),
	(r'^AssReportTestTest/$', AssReportTest),
	(r'^studReportTest/$', studReportTest),
	(r'^auditReportTest/$', auditReportTest),
	(r'^PDFauditReportTest/$', PDFauditReportTest),
	(r'^PDFAssReportTestTest/$', PDFAssReportTest),
	(r'^PDFstudReportTest/$', PDFstudReportTest),
	(r'^CSVauditReportTest/$', CSVauditReportTest),
	(r'^CSVAssReportTestTest/$', CSVAssReportTest),
	(r'^CSVstudReportTest/$', CSVstudReportTest),

	
	#manage assessments
	(r'^assessmentManager/$', AssessmentManager),
	#~ #manage sessions
	#(r'^sessionManager/$', session_manager),

        (r'^getLecturerModules/$', getLecturerModules),

	(r'^assessment/lecturer$', lecturer_assessment),
)
