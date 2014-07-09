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
			marker = request.session['user']
			sessionID = json_data['session_id']
			mark = json_data['mark']
			objID = api.createMarkAllocation(request,leafAssessmentID,marker['uid'],sessionID,student,datetime.today())
			
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
			'type':1,
			'message':'Marked Retrieved',
			'success':'true',
			'marks': list,
		}]
		return HttpResponse(json.dumps(data))
	else:
		data = [
		{
			'type':-1,
			'message':'Request failed',
			'success':'false'
		}]
		return HttpResponse(json.dumps(data))
		
def getStudentsForSession(request):
	if request.method == 'POST':
		try:
			json_data = json.loads(request.body)
			sessionID = json_data['sessionID']
			session = api.getSessionsFromID(sessionID)
			st = api.getStudentsForASession(session)
			person = api.getPersonObjectListFromArrayList(st)
			name = api.getAllNamesOf(person)
			surname = api.getAllSurnameOf(person)
			
			data = [{
				'type':1,
				'message': 'Retrieved student details',
				'uid':st,
				'name':name,
				'surname':surname,
			}]
			return HttpResponse(json.dumps(data))
		except Exception, e:
			data = [{
				'type':-1,
				'message': 'Failed to get student'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return Http404()

def getOpenSessionsForMarker(request):
	if request.method == 'POST':
		try:
			json_data = json.loads(request.body)
			assessmentID = json_data['assessmentID']
			marker = request.session['user']
			openSessions = api.getOpenSessionsForMarker(assessmentID,marker['uid'])
			
			final = []
			
			for x in openSessions:
				list = [] #contains the sessionID and the session name
				list.append(getSessionIdFromObject(x))
				list.append(getSessionNameFromObject(x))
				final.append(list) #an array of all the session id's n manes
			data = [{
				'type':1,
				'message' : 'sessions retrieved',
				'sessions' :final,
			}]
			return HttpResponse(json.dumps(data))
		except Exception, e:
			return Http404()
	else:
		data = [{
				'type':-1,
				'message':'request failed'
			}]
		return HttpResponse(json.dumps(data))

def getAllStudentOfModule(request):
	if request.method == 'POST':
		try:
			json_data = json.loads(request.body)
			mod_code = json_data['mod_code']
			students = api.getAllStudentsOfModule(mod_code)
			stuIDs = api.getAllUidOf(students)
			surnames = api.getAllSurnameOf(students)
			names = api.getAllNamesOf(students)
			
			data = [{
				'type':1,
				'message': 'students retrieved',
				'uid': stuIDs,
				'surnames':surname,
				'names':names,
			}]
			return HttpResponse(json.dumps(data))
		except Exception, e:
			return Http404()
	else:
		data =[{
			'type':-1,
			'message':'error retrieving students',
		}]
		return HttpResponse(json.dumps(data))

def getAllMarkerOfModule(request):
	if request.method == 'POST':
		try:
			json_data = json.loads(request.body)
			mod_code = json_data['mod_code']
			person = getAllMarkersOfModule(mod_code)
			markerIDs = []
			names =[]
			surname = []
			for x in person:
				markerIDs.append(api.getAllUidOf(x))
				names.append(api.getAllNamesOf(x))
				surname.append(api.getAllSurnameOf(x))
			
			data = [{
				'type':1,
				'message':'markers retrieved',
				'uid':markerIDs,
				'names':names,
				'surnames':surname,
			}]
			return HttpResponse(json.dumps(data))
		except Exception, e:
			return Http404()
	else:
		data = [{
			type:-1,
			'message': 'request failed'
		}]
		return HttpResponse(json.dumps(data))
		
def getAllAssessmentOfModule(request):
	if request.method == 'POST':
		try:
			json_data = json.loads(request.body)
			mod_code = json_data['mode_code']
			ass=api.getAllAssessmentsForModule(mode_code)
			assessment = []
			for x in ass:
				list = api.getAssessmentDetails(x) #list consist of the assessment id and name
				assessment.append(list)
			
			data = [{
				'type':1,
				'message': 'assessment retrieved',
				'assessments':assessment
			}]
			return HttpResponse(json.dumps(data))
		except Exception, e:
			return Http404()
	else:
		data = [{
			'type':-1,
			'message': 'failed to retrieve data'
			
		}]
		return HttpResponse(json.dumps(data))

def createSessionForAssessment(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		assID = json_data['assessmentID']
		name = json_data['session_name']
		open = json_data['open_time']
		close = json_data['close_time']
		bool = createSession(request,name,assID,open,close)
		if bool:
			data=[{
				'type':1
				'message':'session created'
			}]
			return HttpResponse(json.dumps(data))
		else:
			data = [{
				'type':-1
				'message':'session not created'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return Http404()
		
def addMarkersToSession(request):
	pass
	
def addSessionToMarker(request):
	pass
	
def deleteSessionFromAssessment(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		
		
# Create your views here.
