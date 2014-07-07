import json
import datetime
from django.http import Http404, HttpResponse
from django.shortcuts import render
from business_logic import api 


def login(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		username =json_data['uid']
		password =json_data['pwd']

		try:
			api.login(request,username,password)
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
	if request.method == 'POST':
		try:
			api.logout(request)
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
			
	
def getStudentModules(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		student =json_data['uid']
		moduleObjects = api.getAllModulesForStudent(student)
		print moduleObjects
		modules = []
		for module in moduleObject:
			modules.append(module)
		data  = [
			{
				'type':1,
				'message':'success',
				'modules':modules
			}
		]
		return HttpResponse(json.dumps(data))
	else:
		raise Http404()
		
def updateMarks(request):
	data = [
	{
		'type':-1,
		'message':'Request failed',
		'success':'false'
	}]
	if request.method == 'POST':
		try:
			json_data =json.loads(request.body)
			student = json_data['uid']
			course = json_data['courseCode']
			leafAssessmentID = json_data['leafAssessmentID']
			mark = json_data['mark']
			markAlloc = api.getMarkAllocationFromID(leafAssessmentID)
			api.updateMarkAllocation(request, markAlloc, mark)
			
			data = [
			{
				'type':1,
				'message':'Mark saved',
				'success':'true'
			}]
			return HttpResponse(json.dumps(data))
		except Exception, e:
			data = [
			{
				'type':-1,
				'message':'Failed to save mark',
				'success':'false'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return HttpResponse(json.dumps(data))
		
def saveMarks(request):
	data = [
	{
		'type':-1,
		'message':'Request failed',
		'success':'false'
	}]
	if request.method == 'POST':
		try:
			json_data =json.loads(request.body)
			student = json_data['uid']
			course = json_data['courseCode']
			leafAssessmentID = json_data['leafAssessmentID']
			marker = json_data['marker']
			sessionID = json_data['session_id']
			mark = json_data['mark']
			objID = api.createMarkAllocation(request,leafAssessmentID,marker,sessionID,student,datetime.today())
			
			data = [
			{
				'type':1,
				'message':'Mark saved',
				'success':'true'
			}]
			return HttpResponse(json.dumps(data))
		except Exception, e:
			data = [
			{
				'type':-1,
				'message':'Failed to save mark',
				'success':'false'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return HttpResponse(json.dumps(data))

def getLeafAssessmentMarkOfAssessment(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		assessment = json_data['assessment']
		student = json_data['uid']
		list = api.getLeafAssessmentMarksOfAsssessmentForStudent(uid,assessment)
		data = [{
			'type':1
			'message':'Marked Retrieved'
			'success':'true'
			'marks': list
		}]
		return HttpResponce(json.dumps(data))
	else:
		data = [
		{
			'type':-1,
			'message':'Request failed',
			'success':'false'
		}]
		return HttpResponce(json.dumps(data))
		
		
	
# Create your views here.
