from django.conf.urls import patterns, include, url
from student import *
	
urlpatterns = patterns('',
	url(r'^getAllMarksForModule$',getAllMarksForModule),
)