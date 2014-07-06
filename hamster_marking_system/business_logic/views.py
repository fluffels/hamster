from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404 
from business_logic.api import *

def login(request):
	username = request.POST['username']
	password = request.POST['password']
	array = login(request,username,password)
	if array:
		return HttpResponse(json.dumps(array), content_type = 'application/json')
	else:
		return HttpResponse(status = 201)
	
def createSessions(request):
	name = request.POST['session_name']
	assess_id = request.POST['assessment_id']
	open = request.POST['open_time']
	close = request.POST['close_time']
	
	bool = createSession(request,name,assess_id,open,close)
	if bool:
		jsonObject = {'session_name':name, 'assessment_id': assess_id, 'open_time': open, 'close_time':close}
		return HttpResponse(json.dumps(jsonObject), mimetype='application/json')
	else:
		return HttpResponse(status= 201)
		
def assignStudent(request):
	list = request.POST['students']
	session_id = request.POST['session_id']
	
	for x in list:
		addStudentToSession(x,session_id)
	return HttpResponse(json.dumps(list))
	
def updateMArk(request):
	mark_id = request.POST['markAllocation_id']
	mark = request.POST['mark']
	
	bool = updateMarkAllocation(request,mark_id,mark)
	if bool:
		return HttpResponse(json.dumps(mark))
	else:
		return HttpResponse(status=201)
	
def viewStudentForSession(request):
	session_id = request.POST['session_id']
	list = addStudentsForASession(session_id)
	if list:
		return HttpResponce(json(list))
	else:
		return HttpResponce(status=200)

def createAssessments(request):
    assess_name = request.POST['asssessment_name']
    assess_type = request.POST['assessment_type']
    mod_code = request.POST['module_code']
    parent_assess = request.POST['parent_assessment']
    assessment_object = createAssessment(request,assess_name, assess_type, mod_code, parent_assess)
    if assessment_object is None:
        message = 'Assessment not created successfully'
        raise Http404  
    else:
        message = 'Assessment created successfully'
    HttpResponse(message)

def assignMarkerInSession(request):
    list_of_chosen_markers = request.POST['chosen_markers']
    session = request.POST['session']
    message = 'Unable to assign marker(s) to session'
    try:
        for marker in list_of_chosen_markers:
            success = setMarkerToSession(request, marker, session) #why are we sending the request with each marker?
            message = 'Markers assigned to session successfully'
    except Exception as e:
        raise Http404
    HttpResponse(message)
    
def awardMark(request):
    student = request.POST['student_number']
    marker = request.POST['marker_id']
    mark_awarded = request.POST['awarded_mark']
    session = request.POST['sessoin_id']
    assessment = request.POST['assessment_id']
    timestamp = request.POST['current_time']
    
    markAlloc = creatMarkAllocation(request, assessment, session, marker, student, timestamp, mark_awarded)
    if markAlloc is None:
        message ='Error. Could not award mark.'
        raise Http404
    else:
        message = 'Mark awarded successfully'
    HttpResponse(message)
    
def viewAllSessions(request):    
    assses = request.POST['asssessment_id']
    
    session_list = getOpenSessions(assess)
    
    if session_list is None:
        return Http404()
    else:
        HttpResponse(session_list)
    
def closeSession(request):
    session = request.POST['session_id']
    
    closed = closeSession(session)
    message = 'Could not close session'
    if closed:
        message = 'Session closed successfully'
    
    HttpResponse(message)
    
    
    
    
    
    
    
    
    
    
    
    
    
    