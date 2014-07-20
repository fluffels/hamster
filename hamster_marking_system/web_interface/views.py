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
        module = request.POST.get('studB')
        print "IN STUDB"
        data=[{
            'mod_code':module,
            'user_type':'tutor'
        }]
        data = views.getAllAssessmentOfModule(request, json.dumps(data))
        print 'haaaaaaaaaaaaaaaaaaaaaaaaaaaahahahhahahahahahahhaahahhhhhhhhhhhhahahahah'
        print data
        result = json.loads(data.content)
        assessmentName = []
        assessmentId = []
        if result[0]['type'] == 1:
            assessments = result[0]['assessments']
            return render_to_response("web_interface/create_assessments_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles, 'assessmentName':assessments,'module':module,'type':1})
        else:
            assessmentName = "There Are No Assessments."
            assessmentId = 0
            return render_to_response("web_interface/create_assessments_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessmentName, 'assessmentId':assessmentId,'module':module,'type':-1})
    elif request.POST.get('tutB'):
        print "IN TUTB"
        module = request.POST.get('tutB')
        data=[{
            'mod_code':module,
            'user_type':'tutor'
        }]
        data = views.getAllAssessmentOfModule(request, json.dumps(data))
        result = json.loads(data.content)
        assessmentName = []
        assessmentId = []
        if result[0]['type'] == 1:
            assessments = result[0]['assessments']
            return render_to_response("web_interface/create_assessments_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessments,'module':module,'type':1})
        else:
            assessmentName = "There Are No Assessments."
            assessmentId = 0
            return render_to_response("web_interface/create_assessments_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessmentName, 'assessmentId':assessmentId,'module':module,'type':-1})
    elif request.POST.get('taB'):
        print "IN TAB"
        module = request.POST.get('taB')
        data=[{
            'mod_code':module,
            'user_type':'tutor'
        }]
        data = views.getAllAssessmentOfModule(request, json.dumps(data))
        result = json.loads(data.content)
        assessmentName = []
        assessmentId = []
        if result[0]['type'] == 1:
            assessments = result[0]['assessments']
            return render_to_response("web_interface/create_assessments_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessments,'module':module,'type':1})
        else:
            assessmentName = "There Are No Assessments."
            assessmentId = 0
            return render_to_response("web_interface/create_assessments_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessmentName, 'assessmentId':assessmentId,'module':module,'type':-1})
    elif request.POST.get('lectB'):
        print "IN LECTB"
        module = request.POST.get('lectB')
        data=[{
            'mod_code':module,
            'user_type':'tutor'
        }]
        data = views.getAllAssessmentOfModule(request, json.dumps(data))
        result = json.loads(data.content)
        assessmentName = []
        assessmentId = []
        if result[0]['type'] == 1:
            assessments = result[0]['assessments']
            return render_to_response("web_interface/create_assessments_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessments,'module':module,'type':1})
        else:
            assessmentName = "There Are No Assessments."
            assessmentId = 0
            return render_to_response("web_interface/create_assessments_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessmentName, 'assessmentId':assessmentId,'type':-1})

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
        return render_to_response("web_interface/create_sessions_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'sessions':sessions,'assessmentName':assessmentName,'moduleName':moduleName,'assessment_id':assess})
    else:
        list = []
        list.append('-1')
        list.append('session data not found')
        sessions.append(list)
        assessmentName = sess[0]['assessmentName']
        moduleName=sess[0]['moduleName']
        return render_to_response("web_interface/create_sessions_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'sessions':sessions,'assessment_id':assess,'assessmentName':assessmentName,'moduleName':moduleName})

@csrf_exempt
def createAssessment(request):
    assessName = request.POST['name']
    mod = request.POST['mod']
    fullmark = request.POST['fullmark']
    assess_id = request.POST['leaf']
    
    data = {
        'name':assessName,
        'mod':mod,
        'fullmark':fullmark,
        'assess_id': assess_id
    }
    res= views.createAssessment(request,json.dumps(data))
    results = json.loads(res.content)
    if results[0]['type'] == 1:
        assess = results[0]['assessment']
        return render_to_response("web_interface/create_assessments_lect.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                           'user_roles':user_roles,'assessmentName':assess,"module":mod,'type':1})
    else:
        return render_to_response("web_interface/login.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                           'user_roles':user_roles})

@csrf_exempt
def createSession(request):
    assess_id = request.POST['assess_id']
    open_time = request.POST['open_time']
    close_time = request.POST['close_time']
    name = request.POST['name']
    
    data ={
        'assess_id':assess_id,
        'name':name,
        'open_time': open_time,
        'close_time':close_time
    }
    res = views.createSessionForAssessment(request,json.dumps(data))
    results = json.loads(res.content)
    
    if results[0]['type'] == 1:
        assess_name = results[0]['assessmentName']
        sessions = results[0]['sessions']
        mod = results[0]['mod']
        return render_to_response("web_interface/create_sessions_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'sessions':sessions,'assessmentName':assess_name,'assessment_id':assess_id,'moduleName':mod})

    else:
        assess_name = results[0]['assessmentName']
        sessions = results[0]['sessions']
        mod = results[0]['mod']
        return render_to_response("web_interface/create_sessions_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'sessions':sessions,'assessmentName':assess_name,'assessment_id':assess_id,'moduleName':mod})
@csrf_exempt
def searchForStudent(request):
    user_query = request.POST['query']
    
    data ={
        'query':user_query,

    }
    peopleWanted = views.searchForStudent(request,json.dumps(data))
    peopleFound = json.loads(peopleWanted.content)
    
    if peopleFound[0]['type'] == 1:
        list_of_people = peopleFound[0]['users']
        return render_to_response("web_interface/add_user_to_session.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'list_of_people':list_of_people})

@csrf_exempt
def getAllStudentOfModule(request):
    mod = request.POST['module']
    session = request.POST['session']

    data = {
        'module':mod,
        'session':session
    }
    info = views.getAllStudentForModule(request,json.dumps(data))
    res = json.loads(info.content)
    
    if res[0]['type'] == 1:
        students = res[0]['students']
        ta = res[0]['ta']
        tut = res[0]['tut']
        name = res[0]['name']
        return render_to_response("web_interface/add_user_to_session.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'students':students,'module':mod,'session_id':session,'tutor':tut,'teachingA':ta,'sessionName':name})
    else:
        students = []
        ta = []
        tut = []
        return render_to_response("web_interface/add_user_to_session.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'students':students,'module':mod,'session_id':session,'tutor':tut,'teachingA':ta,'sessionName':name})

@csrf_exempt
def addStudentToSession(request):
    mod = request.POST['submit']
    session_id = request.POST['session']
    users = request.POST.lists()
    print "]]]]]]]]]]]]]]]]]]"
    print users
    # users[1][1][0]
    Studentarray = []
    MarkerArray = []
    if users[1][0] == 'userS':
        print users[1][0]
        for n in users[1][1]:
            Studentarray.append(n)
    else:
        for n in users[1][1]:
            MarkerArray.append(n)
    
    data = {
        'student':Studentarray,
        'marker':Studentarray,
        'session':session_id	
    }
    results = views.addUserToSession(request,json.dumps(data))
    res = json.loads(results.content)
    if res[0]['type'] == 1:
        name = res[0]['name']
        students = res[0]['students']
        marker = res[0]['marker']
        return render_to_response("web_interface/added_user_to_session.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'students':students,
                                                                        'module':mod,'session_id':session_id,
                                                                        'sessionName':name,'marker':marker})
@csrf_exempt
def getAllPersonOfSession(request):
    mod = request.POST['mod']
    session_id = request.POST['session']
    Studentarray = []
    MarkerArray = []
    
    data ={
        'session_id':session_id
    }
    result = views.getAllPersonOfSession(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] == 1:
        sessionName = res[0]['name']
        students = res[0]['students']
        marker = res[0]['marker']
        
        return render_to_response("web_interface/added_user_to_session.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'students':students,
                                                                        'module':mod,'session_id':session_id,
                                                                        'sessionName':sessionName,'marker':marker})
    else:
        return render_to_response("web_interface/added_user_to_session.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'students':[],
                                                                        'module':mod,'session_id':session_id,
                                                                        'sessionName':'An error occurred, a session was not found!','marker':[]})

@csrf_exempt
def getAllChildrenOfAssessment(request):
    assess_id = request.POST['assessment']
    mod = request.POST['mod']
    
    data = {
        'assess_id':assess_id,
        'mod':mod
    }
    results = views.getAllChildrenOfAssessment(request,json.dumps(data))
    res = json.loads(results.content)
    if res[0]['type'] == 1:
        if res[0]['message'] == 'Aggregate':
            child = res[0]['child']
            name = res[0]['name']
            return render_to_response("web_interface/view_aggregate_assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'child':child,
                                                                        'module':mod,'assessmentName':name,'assess_id':assess_id})
        
        else:
            studentMark = res[0]['studentMark']
            name = res[0]['name']
            fullmark = res[0]['fullmark']
            return render_to_response("web_interface/view_leaf_assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'studentMark':studentMark,
                                                                        'module':mod,'assessmentName':name,'assess_id':assess_id,'fullmark':fullmark})

@csrf_exempt
def createLeafAssessment(request):
    assessName = request.POST['name']
    mod = request.POST['mod']
    fullmark = request.POST['fullmark']
    assess_id = request.POST['leaf']
    
    data = {
        'name':assessName,
        'mod':mod,
        'fullmark':fullmark,
        'assess_id': assess_id
    }
    res= views.createLeafAssessment(request,json.dumps(data))
    results = json.loads(res.content)
    if results[0]['type'] == 1:
        assess = results[0]['assessment']
        name = results[0]['name']
        assess_id = results[0]['assess_id']
        
        return render_to_response("web_interface/view_aggregate_assessments.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                           'user_roles':user_roles,'assessmentName':name,"module":mod,'child':assess,'assess_id':assess_id})
    else:
        return render_to_response("web_interface/login.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                           'user_roles':user_roles})
@csrf_exempt
def updateMarkForStudent(request):
    leaf_id = request.POST['assess_id']
    mark = request.POST['mark']
    student = request.POST['uid']
    mod = request.POST['mod']
    
    data = {
        'leaf_id':leaf_id,
        'mark':mark,
        'student':student,
        'mod':mod
    }
    
    result = views.updateMarkForStudent(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] == 1:
        studentMark = res[0]['studentMark']
        name = res[0]['name']
        fullmark = res[0]['fullmark']
        return render_to_response("web_interface/view_leaf_assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'studentMark':studentMark,
                                                                        'module':mod,'assessmentName':name,'assess_id':leaf_id,'fullmark':fullmark,'message':1})
    else:
        studentMark = res[0]['studentMark']
        name = res[0]['name']
        fullmark = res[0]['fullmark']
        return render_to_response("web_interface/view_leaf_assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'studentMark':studentMark,
                                                                        'module':mod,'assessmentName':name,'assess_id':leaf_id,'fullmark':fullmark,'message':0})
@csrf_exempt
def deleteAssessment(request):
    assess_id = request.POST['assess_id']
    mod = request.POST['mod']
    
    data = {
        'assess_id':assess_id,
    }
    result = views.deleteAssessment(request,json.dumps(data))
    res = json.loads(result.content)
    
    if res[0]['type'] == 1:
        if res[0]['isMod'] == True:
            data=[ {
                'mod_code':mod
            }]
            assess = views.getAllAssessmentOfModule(request,json.dumps(data))
            print "Assessments of module : " + str(assess)
            ass = json.loads(assess.content)
            if ass[0]['type'] == 1:
                assessment = ass[0]['assessments']
                return render_to_response("web_interface/create_assessments_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles, 'assessmentName':assessment,'module':mod,'type':1})
            else:
                assessmentName = "There Are No Assessments."
                assessmentId = 0
                return render_to_response("web_interface/create_assessments_lect.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessmentName, 'assessmentId':assessmentId,'module':mod,'type':-1})
        else:
            assessment = res[0]['assess_id']
            data={
                'assess_id':assessment,
                'mod':mod
            }
            children = views.getAllChildrenOfAssessment(request,json.dumps(data))
            child = json.loads(children.content)
            if child[0]['type'] == 1:
                if child[0]['message'] == 'Aggregate':
                    child1 = child[0]['child']
                    name = child[0]['name']
                    return render_to_response("web_interface/view_aggregate_assessments.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'child':child1,
                                                                                'module':mod,'assessmentName':name,'assess_id':assessment})

                else:
                    studentMark = child[0]['studentMark']
                    name = child[0]['name']
                    fullmark = child[0]['fullmark']
                    return render_to_response("web_interface/view_leaf_assessments.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'studentMark':studentMark,
                                                                                'module':mod,'assessmentName':name,'assess_id':assessment,'fullmark':fullmark})

@csrf_exempt
def deleteSession(request):
    sess_id = request.POST['session']
    assess_id = request.POST['assessment']
    mod = request.POST['mod']
    
    data = {
        'sessionId':sess_id
    }
    
    info = views.deleteSession(request,json.dumps(data))
    res = json.loads(info.content)
    
    if res[0]['type'] == 1:
        data = {
            'assessmentID':assess_id
        }
        session = views.getAllSessionsForAssessment(request,json.dumps(data))
        sess = json.loads(session.content)
        sessions = []
        if sess[0]['type'] == 1:
            sessions = sess[0]['sessions']
            assessmentName = sess[0]['assessmentName']
            moduleName=mod
            return render_to_response("web_interface/create_sessions_lect.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'user_roles':user_roles,'sessions':sessions,'assessmentName':assessmentName,'moduleName':moduleName,'assessment_id':assess_id,'message':1})
        else:
            list = []
            list.append('-1')
            list.append('session data not found')
            sessions.append(list)
            assessmentName = sess[0]['assessmentName']
            moduleName=mod
            return render_to_response("web_interface/create_sessions_lect.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'user_roles':user_roles,'sessions':sessions,'assessment_id':assess_id,'assessmentName':assessmentName,'moduleName':moduleName,'message':1})
    else:
        data = {
            'assessmentID':assess_id
        }
        session = views.getAllSessionsForAssessment(request,json.dumps(data))
        sess = json.loads(session.content)
        sessions = []
        if sess[0]['type'] == 1:
            sessions = sess[0]['sessions']
            assessmentName = sess[0]['assessmentName']
            moduleName=mod
            return render_to_response("web_interface/create_sessions_lect.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'user_roles':user_roles,'sessions':sessions,'assessmentName':assessmentName,'moduleName':moduleName,'assessment_id':assess_id,'message':0})
        else:
            list = []
            list.append('-1')
            list.append('session data not found')
            sessions.append(list)
            assessmentName = sess[0]['assessmentName']
            moduleName=mod
            return render_to_response("web_interface/create_sessions_lect.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'user_roles':user_roles,'sessions':sessions,'assessment_id':assess_id,'assessmentName':assessmentName,'moduleName':moduleName,'message':0})

@csrf_exempt
def changeAssessmentFullMark(request):
    assess_id = request.POST['assess_id']
    mod = request.POST['mod']
    mark = request.POST['fullmark']
    
    data = {
        'assess_id':assess_id,
        'full_mark':mark
    }
    result = views.changeAssessmentFullMark(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] == 1:
        data={
                'assess_id':assess_id,
                'mod':mod
        }
        children = views.getAllChildrenOfAssessment(request,json.dumps(data))
        child = json.loads(children.content)
        if child[0]['type'] == 1:
            if child[0]['message'] == 'leaf':
                studentMark = child[0]['studentMark']
                name = child[0]['name']
                fullmark = child[0]['fullmark']
                return render_to_response("web_interface/view_leaf_assessments.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'studentMark':studentMark,
                                                                                'module':mod,'assessmentName':name,'assess_id':assess_id,'fullmark':fullmark})
