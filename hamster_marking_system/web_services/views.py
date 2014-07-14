import json
import datetime
from django.http import Http404, HttpResponse
from django.shortcuts import render
from business_logic import api 
from django.core.context_processors import csrf


def login(request,jsonObj):
	#if request.method == 'POST':
	json_data = json.loads(jsonObj)
	username =json_data['username']
	password =json_data['password']

	try:
		usr = api.login(request,username,password)
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
	'''else:
		data =[
			{
				'type':-1,
				'message': 'Login failed. Request invalid'
			}
		]
		return HttpResponse(json.dumps(data))'''
		
def logout(request):
	#if request.method == 'POST':
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
		
def getAllAssessmentOfModule(request,jsonData):
#	if request.method == 'POST':
		print "web service views"
		try:
			json_data = json.loads(jsonData)
			print json_data
			mod_code = json_data[0]['mod_code']
			print mod_code
			print "web service views1"
			ass=api.getAllAssessmentsForModule(mod_code)
			print "web service views2"
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
			data = [{
				'type':-1,
				'message': 'assessment could not be retrieved'
			}]
			print "What happened Mamelo?"
			print json.dumps(data)
			return HttpResponse(json.dumps(data))

			'''
	else:
		data = [{
			'type':-1,
			'message': 'failed to retrieve data'
			
		}]
		return HttpResponse(json.dumps(data))
	'''

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
				'type':1,
				'message':'session created'
			}]
			return HttpResponse(json.dumps(data))
		else:
			data = [{
				'type':-1,
				'message':'session not created'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return Http404()

	
def addMarkersToSession(request):
	pass
	
def addSessionToMarker(request):
	pass

def removeMarkerFromSession(request):
	pass
	
def removeStudentFromSession(request):
	pass
	
def deleteSessionFromAssessment(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		sessionID = json_data['sessionID']
		bool = api.removeSession(request,sessionID)
		if bool:
			data=[{
				'type':1,
				'message': 'session deleted'
			}]
			return HttpResponse(json.dumps(data))
		else:
			data=[{
				
			'type':-1,
			'message': 'request failed'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return Http404()

def openSession(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		sessionID = json_data['sessionID']
		bool = api.closeSession(sessionID)
		if bool:
			data = [{
				'type':1,
				'message': 'session opened'
			}]
			return HttpResponse(json.dumps(data))
		else:
			data = [{
				'typr':-1,
				'message': 'request failed'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return Http404()
		
def closeSession(request):
	if request.method =='POST':
		json_data = json.loads(request.body)
		sess = json_data['sessionID']
		bool = api.closeSession(sess)
		if bool:
			data = [{
				'type':1,
				'message':'session closed'
			}]
			return HttpResponse(json.dumps(data))
		else:
			data=[{
				'type':-1,
				'message':'request failed'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return Htpp404()
		
def removeMarkerFromModule(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		marker = json_data['uid']
		mod_code = json_data['mod_code']
		bool = api.removeMarkerFromModule(request,mod_code,marker)
		if bool:
			data =[{
				'type':1,
				'message': 'marker removed'
			}]
			return HttpResponse(json.dumps(data))
		else:
			data =[{
				'type':-1,
				'message':'request failed'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return Http404()

def setTAforModule(request):
	if request.method =='POST':
		json_data = json.loads(request.body)
		mod_code= json_data['mod_code']
		uid = json_data['uid']
		ta = api.setTeachingAssistantForModule(request,uid,mod_code)
		if ta:
			data =[{
				'type':1,
				'message':'ta inserted'
			}]
			return HttpResponse(json.dumps(data))
		else:
			data =[{
				'type':-1,
				'message':'request failed'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return Http404()
		
def setTutorForModule(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		mod = json_data['mode_code']
		uid = json_data['uid']
		ta = api.setTutorForModule(request,uid,mod)
		if ta:
			data = [{
				'type':1,
				'message':'tutor inserted'
			}]
			return HttpResponse(json.dumps(data))
		else:
			data = [{
				'type':-1,
				'message':'request failed'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return Http404()

def createAssessment(request):
	pass

def personDetails(request):
#	json_data = json.loads(jsonObject)
	try:
	     per = request.session['user']['uid']
	     person = api.getPersonDetails(per[0])
	     cn = person['cn'][0]
	     title = person['title'][0]
	     sn = person['sn'][0]
	     initials = person['initials'][0]
	     
	     if person:
	              data = [{
	                      'type':1,
	                      'message':'person data retrieved',
	                      'name':cn,
	                      'title':title,
	                      'surname':sn,
	                      'initials':initials
	                }]
	              return HttpResponse(json.dumps(data))
	     else:
	        data = [{
	                      'type':-1,
	                      'message':'person data retrieved'
	                }]
	        return HttpResponse(json.dumps(data))
	except Exception, e:
		data = [{
			      'type':-1,
			      'message':'person data retrieved'
			}]
		return HttpResponse(json.dumps(data))

def getAllSessionsForAssessment(request,jsonObject):
	json_data = json.loads(jsonObject)
	assessID = json_data['assessmentID']
	print assessID
	info = api.getAllSessionsForAssessment(assessID)
	print "passed"
	print info
	session =[]
	if len(info) != 0:
		print info
		for x in info:
			
			list = api.getSessionDetails(x)
			session.append(list)
			
		assess= api.getAssessmentName(assessID)
		mod = api.getModuleNameForAssessment(assessID)
		data = [{
			'type':1,
			'message':'session retrieved',
			'sessions':session,
			'assessmentName': assess,
			'moduleName':mod
		}]
		return HttpResponse(json.dumps(data))
	else:
		print "error"
		data = [{
			'type':-1,
			'message':'error occured'
		}]
		return HttpResponse(json.dumps(data))
# Create your views here.