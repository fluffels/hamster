from django.conf.urls import patterns, include, url
from user import *
	
urlpatterns = patterns('',
	url(r'^login$', login),
	url(r'^logout$', logout),
)