from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import SquirrelMarking.businessLogicAPI as BL
import json

'''
Function: login
Deescription: Authenticate users login details

@type: String
@param: A http request for validation of the users login details

@type: String
@return: A http responce containing required data if the user was successfuly login and return 
	     a confirmation of failer if the user was not successfuly login
'''
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

'''
Function: logout
Deescription: The user is logged out of the  server

@type: String
@param: A http request to logout the user

@type: String
@return: A http responce confirming if the user was successfuly logout or not
'''
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