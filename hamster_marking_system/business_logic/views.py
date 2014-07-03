from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404 
from business_logic.api import *

def createAssessments(request):
    assess_name = request.POST['asssessment_name']
    assess_type = request.POST['assessment_type']
    mod_code = request.POST['module_code']
    parent_assess = request.POST['parent_assessment']
    
    assessment_object = createAssessment(request,assess_name, assess_type, mod_code, parent_assess)
    
    if assessment_object is None:
        message = 'Assessment not created successfully'   
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
        pass
        
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    