import json
import urllib2
from django.shortcuts import render, render_to_response, RequestContext
from web_services import views
from django.views.decorators.csrf import csrf_exempt
from django.template import loader

def home(request):
    return render_to_response("web_interface/login.htm",
                              locals(),
                              context_instance = RequestContext(request))
@csrf_exempt
def login(request):
	user = request.POST['username']
	passw = request.POST['password']
	data = {
		'username':user,
		'password':passw
	}
	user_info = views.login(request,json.dumps(data))
	#user_info = urllib2.urlopen('/login',json.dumps(data))
	user = json.loads(user_info.content)
	user_type = ''
	global default_user
	default_user =''
	global user_roles
	user_roles = []
	
	global user_lect
	user_lect = []
	global user_stud
	user_stud = []
	global user_tut
	user_tut = []
	global user_ta
	user_ta = []
	if user[0]['type'] == 1:
		if len(user[0]['lecturerOf']) != 0:
			user_type = 'LC'
			user_lect.append({user_type:user[0]['lecturerOf']})
			user_roles.append('Lecturer')
			
		if len(user[0]['studentOf']) != 0:
			user_type ='ST'
			user_stud.append({user_type:user[0]['studentOf']})
			user_roles.append('Student')
			
		if len(user[0]['tutorFor']) != 0:
			user_type = 'TT'
			user_tut.append({user_type:user[0]['tutorFor']})
			user_roles.append('Tutor')
			
		if len(user[0]['teachingAssistantOf']) != 0:
			user_type ='TA'
			user_ta.append({user_type:user[0]['teachingAssistantOf']})
			user_roles.append('Teaching ass')
		
		#choosing the default user based on the user type ie,lecturer
		if len(user[0]['lecturerOf']) != 0:
		    default_user = 'LC'
		elif len(user[0]['studentOf']) != 0:
		    default_user = 'ST'
		elif len(user[0]['tutorFor']) != 0:
		    default_user = 'TT'
		else:
		    default_user = 'TA'
		    
		return render_to_response("web_interface/success.htm",{'default_user':default_user,
								       'user_lect':user_lect,
								       'user_stud':user_stud,
								       'user_tut':user_tut,
								       'user_ta':user_ta,
								    'user_roles':user_roles})
	else:
		return render_to_response("web_interface/login.htm",locals(),context_instance = RequestContext(request))

def logout(request):
	user_info = views.logout(request)
	user = json.loads(user_info.content)
	if user[0]['type'] == 1:
		 return render_to_response("web_interface/base_template.htm",locals(),context_instance = RequestContext(request))
	else:
		return render_to_response("web_interface/success.htm",locals(),context_instance = RequestContext(request))

@csrf_exempt
def getAllAssessmentOfModule(request):
    if request.POST.get('studB'):
        print "IN STUDB"
        data=[{
            'mod_code':request.POST.get('studB'),
            'user_type':'tutor'
        }]
        data = views.getAllAssessmentOfModule(request, json.dumps(data))
        result = json.loads(data.content)
        assessmentName = []
        assessmentId = []
        if result[0]['type'] == 1:
            assessments = result[0]['assessments']
            return render_to_response("web_interface/assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles, 'assessmentName':assessments})
        else:
            assessmentName = "There Are No Assessments."
            assessmentId = 0
            return render_to_response("web_interface/assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessmentName, 'assessmentId':assessmentId})
    elif request.POST.get('tutB'):
        print "IN TUTB"
        data=[{
            'mod_code':request.POST.get('tutB'),
            'user_type':'tutor'
        }]
        data = views.getAllAssessmentOfModule(request, json.dumps(data))
        result = json.loads(data.content)
        assessmentName = []
        assessmentId = []
        if result[0]['type'] == 1:
            assessments = result[0]['assessments']
            return render_to_response("web_interface/assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessments})
        else:
            assessmentName = "There Are No Assessments."
            assessmentId = 0
            return render_to_response("web_interface/assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessmentName, 'assessmentId':assessmentId})
    elif request.POST.get('taB'):
        print "IN TAB"
        data=[{
            'mod_code':request.POST.get('taB'),
            'user_type':'tutor'
        }]
        data = views.getAllAssessmentOfModule(request, json.dumps(data))
        result = json.loads(data.content)
        assessmentName = []
        assessmentId = []
        if result[0]['type'] == 1:
            assessments = result[0]['assessments']
            return render_to_response("web_interface/assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessments})
        else:
            assessmentName = "There Are No Assessments."
            assessmentId = 0
            return render_to_response("web_interface/assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessmentName, 'assessmentId':assessmentId})
    elif request.POST.get('lectB'):
        print "IN LECTB"
        data=[{
            'mod_code':request.POST.get('lectB'),
            'user_type':'tutor'
        }]
        data = views.getAllAssessmentOfModule(request, json.dumps(data))
        result = json.loads(data.content)
        assessmentName = []
        assessmentId = []
        if result[0]['type'] == 1:
            assessments = result[0]['assessments']
            return render_to_response("web_interface/assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessments})
        else:
            assessmentName = "There Are No Assessments."
            assessmentId = 0
            return render_to_response("web_interface/assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessmentName, 'assessmentId':assessmentId})

def personDetails(request):
    web = views.personDetails(request)
    results = json.loads(web.content)
    if results[0]['type'] == 1:
        name = results[0]['name']
        surname = results[0]['surname']
        title = results[0]['title']
        initials = results[0]['initials']
        return render_to_response("web_interface/person_details.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'name':name,'surname':surname,'title':title,'initials':initials})
    else:
        return render_to_response("web_interface/person_details.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'name':'person data not found'})

@csrf_exempt
def getAllSessionsForAssessment(request):
    assess = request.POST['assessment']
    data = {
        'assessmentID':assess
    }
    res = views.getAllSessionsForAssessment(request,json.dumps(data))
    sess = json.loads(res.content)
    sessions = []
    print sess
    if sess[0]['type'] == 1:
        sessions = sess[0]['sessions']
        assessmentName = sess[0]['assessmentName']
        moduleName=sess[0]['moduleName']
        return render_to_response("web_interface/view_session.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'sessions':sessions,'assessmentName':assessmentName,'moduleName':moduleName})
    else:
        list = []
        list.append('-1')
        list.append('session data not found')
        sessions.append(list)
        return render_to_response("web_interface/view_session.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'sessions':sessions})

