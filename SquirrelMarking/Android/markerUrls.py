from django.conf.urls import patterns, include, url
from marker import *
	
urlpatterns = patterns('',
	url(r'^getTaskListByAssessment$',getTaskListByAssessment),
	url(r'^getActiveAssessments$',getActiveAssessments),
	url(r'^saveMarks$',saveMarks),
	url(r'^getStudentsToMark$',getStudents),
)