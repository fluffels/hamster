from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import SquirrelMarking.businessLogicAPI as BL
import json

def login(request):	
	if request.method == 'GET':
		#print("Method: " +request.method)
		username = request.GET['uid']
		password = request.GET['pwd']
		#json_data = json.loads(request.body)
		#username =json_data['uid']
		#password =json_data['pwd']
		#print username + " - " + password
		#print "User object "
		#print request.session['user']

		try:
			BL.login(request,username,password)
			usr =request.session['user']
			data = [{
				"type":1,
				"message":"User logged in",
				"cn": usr.get('cn'), 
	  			"uid": usr.get('uid'),
				"title": usr.get('title'), 
				"lecturerOf": usr.get('lecturerOf'), 
				"teachingAssistantOf": usr.get('teachingAssistantOf'), 
				"sn": usr.get('sn'), 
				"tutorFor": usr.get('tutorFor'), 
				"studentOf": usr.get('studentOf'),
				"initials": usr.get('initials')
			}]
			return HttpResponse(json.dumps(data), content_type="application/json")
		except Exception, e:
			data =[
				{
					'type':-1,
					'message':'login failed. Server exception'
				}
			]
			return HttpResponse(json.dumps(data)) 
	else:
		data =[
			{
				'type':-1,
				'message': 'Login failed. Request invalid'
			}
		]
		return HttpResponse(json.dumps(data))


def logout(request):
	if request.method == 'GET':
		try:
			BL.logout(request)
			data =[
			{
				'type': 1,
				'message':'Logout successful'
			}]
			return HttpResponse(json.dumps(data))
		except Exception, e:
			data = [
			{
				'type':-1,
				'message':'Logout failed. Server exception'
			}]
			return HttpResponse(json.dumps(data))