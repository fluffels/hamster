import json
import urllib2
from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from web_services import views
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, RequestContext
from .decorators import isAuthenticated, isLecture, isMarker, isStudent, isPartOfmodule
from django.contrib.auth.models import User
from recaptcha.client import captcha
from reporting import views as repo


#default_user = []
#user_roles = []
#user_lect = []
#user_stud = []
#user_tut = []
#user_ta = []

def home(request):
    return render_to_response("web_interface/login.htm",
                              locals(),
                              context_instance = RequestContext(request))

def reCaptchaLogin(request):      
    # talk to the reCAPTCHA service  
    response = captcha.submit(  
        request.POST.get('recaptcha_challenge_field'),  
        request.POST.get('recaptcha_response_field'),  
        '6Leu-PsSAAAAAFcLbrwJocmUAJDl4Vt62-CA1rnN',  
        request.META['REMOTE_ADDR'],)
    
        
    user_ip = request.POST['user_ip']
    login_count = request.POST['login_count']
    if(login_count == ''):
        login_count = 0
    current_ip = request.META['REMOTE_ADDR']
    if(user_ip == ''):
        user_ip = current_ip

    if (user_ip == current_ip):
        login_count = int(login_count) + 1
    
    print "LOGIN_COUNT : " + str(login_count)
    print "IP ADDRESS : " + str(user_ip)
    print "CURR IP ADDRES : " + str(current_ip)
    # see if the user correctly entered CAPTCHA information  
    # and handle it accordingly.  
    if response.is_valid:
        #User is human, so reset login count
        try:
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
           # global default_user
            default_user =''
            #global user_roles
            user_roles = []

            #global user_lect
            user_lect = []
           # global user_stud
            user_stud = []
            #global user_tut
            user_tut = []
            #global user_ta
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
    
                    Users = user[0]['Users']
                    Modules = user[0]['Modules']
                    
                    username = request.session['user']['uid'][0]
                    name = request.session['user']['cn'][0]
                    surname = request.session['user']['sn'][0]
                    try:
                        print User.objects.all()
                        user = User.objects.get(username=username,first_name=name,last_name=surname)
                        print "User : " + str(user)
                        if user:
                            if user.is_superuser:
                                return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'Person':Users,
                                                                            'Modules':Modules,
                                                                            'user_roles':user_roles, 'user_ip':'0.0.0.0', 'login_count':0},context_instance = RequestContext(request))
                    except Exception, ex:
                        print "Could not find user in User's"
                        user = None
                        print "User X: " + str(user)
    
                    return render_to_response("web_interface/success.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'user_roles':user_roles, 'user_ip':'0.0.0.0', 'login_count':0},context_instance = RequestContext(request))
            else:
                    return render_to_response("web_interface/login.htm",{'type':-1, 'user_ip':user_ip, 'login_count':login_count},context_instance = RequestContext(request))
        except Exception  as e:
            raise Http404()  
    else:  
        captcha_response = 'YOU MUST BE A ROBOT'  
        return render_to_response('web_interface/login.htm', {  
                'type':-1,  
                'captcha_response': captcha_response, 'user_ip':user_ip, 'login_count':login_count}
                                ,context_instance = RequestContext(request))
      

def login(request):
    #try:
        user = request.POST['username']
        passw = request.POST['password']
        user_ip = request.POST['user_ip']
        login_count = request.POST['login_count']
        if(login_count == ''):
            login_count = 0
        current_ip = request.META['REMOTE_ADDR']
        if(user_ip == ''):
            user_ip = current_ip

        if (user_ip == current_ip):
            login_count = int(login_count) + 1

        print "LOGIN_COUNT : " + str(login_count)
        print "IP ADDRESS : " + str(user_ip)
        print "CURR IP ADDRES : " + str(current_ip)

        data = {
                'username':user,
                'password':passw
        }
        user_info = views.login(request,json.dumps(data))
        #user_info = urllib2.urlopen('/login',json.dumps(data))
        user = json.loads(user_info.content)
        user_type = ''
        #global default_user
        default_user =''
        #global user_roles
        user_roles = []
        
       # global user_lect
        user_lect = []
        #global user_stud
        user_stud = []
        #global user_tut
        user_tut = []
        #global user_ta
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

		Users = user[0]['Users']
		Modules = user[0]['Modules']
		
		username = request.session['user']['uid'][0]
		name = request.session['user']['cn'][0]
		surname = request.session['user']['sn'][0]
		try:
		    print User.objects.all()
		    user = User.objects.get(username=username,first_name=name,last_name=surname)
		    print "User : " + str(user)
		    if user:
		        if user.is_superuser:
		            return render_to_response("web_interface/admin.htm",{'default_user':default_user,
		                                                       'user_lect':user_lect,
		                                                       'user_stud':user_stud,
		                                                       'user_tut':user_tut,
		                                                       'user_ta':user_ta,
		                                                       'Person':Users,
		                                                       'Modules':Modules,
		                                                       'user_roles':user_roles, 'user_ip':'0.0.0.0', 'login_count':0},context_instance = RequestContext(request))
		except Exception, ex:
		    print "Could not find user in User's"
		    user = None
		    print "User X: " + str(user)

                return render_to_response("web_interface/success.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'user_roles':user_roles, 'user_ip':'0.0.0.0', 'login_count':0},context_instance = RequestContext(request))
        else:
                 return render_to_response("web_interface/login.htm",{'type':-1, 'user_ip':user_ip, 'login_count':login_count},context_instance = RequestContext(request))
    #except Exception  as e:
        #raise Http404()


@isAuthenticated
def backHome(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    return render_to_response("web_interface/success.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))

@isAuthenticated
def use_as(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    role = request.POST['role']
    if role == 'Student':
        lect = 'LT'
        tut = 'TT'
        ta = 'TA'
        return render_to_response("web_interface/success.htm",{'default_user':default_user,
                                                                        'user_lect':lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':tut,
                                                                        'user_ta':ta,
                                                                        'user_roles':user_roles},context_instance = RequestContext(request))
    elif role == 'Lecturer':
        stud = 'ST'
        tut = 'TT'
        ta = 'TA'
        return render_to_response("web_interface/success.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':stud,
                                                                       'user_tut':tut,
                                                                       'user_ta':ta,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))
    elif role == 'Tutor':
        lect = 'LT'
        stud = 'ST'
        ta = 'TA'
        return render_to_response("web_interface/success.htm",{'default_user':default_user,
                                                                       'user_lect':lect,
                                                                       'user_stud':stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':ta,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))
    else:
        lect = 'LT'
        stud = 'ST'
        tut = 'TT'
        return render_to_response("web_interface/success.htm",{'default_user':default_user,
                                                                       'user_lect':lect,
                                                                       'user_stud':stud,
                                                                       'user_tut':tut,
                                                                       'user_ta':user_ta,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))

def logout(request):
	user_info = views.logout(request)
	user = json.loads(user_info.content)
	if user[0]['type'] == 1:
		return HttpResponseRedirect(reverse('home'))
	else:
		return HttpResponseRedirect(reverse('home'))

@isAuthenticated
@isPartOfmodule
def getAllAssessmentOfModule(request,module):
    
        user_type = ''
        # global default_user
        default_user =''
        #global user_roles
        user_roles = []
        #global user_lect
        user_lect = []
        # global user_stud
        user_stud = []
        #global user_tut
        user_tut = []
        #global user_ta
        user_ta = []
        user = request.session['user']
    
        if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
        if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
        if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
        if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
        #choosing the default user based on the user type ie,lecturer
        if len(user['lecturerOf']) != 0:
            default_user = 'LC'
        elif len(user['studentOf']) != 0:
            default_user = 'ST'
        elif len(user['tutorFor']) != 0:
            default_user = 'TT'
        else:
            default_user = 'TA'

        if request.POST.get('studB'):
            mod = request.POST['studB'];
            data ={
                'module':mod
            }
            result = views.testingStudentAssessmentForModule(request,json.dumps(data))
            res = json.loads(result.content)
            print "-=-=-=-=-=-=-=-=--=-=-=-=-"+str(res)
            if res[0]['type'] == '1':
                print "something"
                root = res[0]['root']
                first = res[0]['first']
                second = res[0]['second']
                third = res[0]['third']
                print "root"+ str(root)
                print "---------------------------------------------------------------"
                print "first"+str(first)
                print "---------------------------------------------------------------"
                print "second"+str(second)
                print "---------------------------------------------------------------"
                print "third" + str(third)
                return render_to_response("web_interface/view_student_marks.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'root':root,'first':first,
                                                                                'module':mod,'second':second,'third':third,},context_instance = RequestContext(request))
            else:
                print "NONE"
                root = "NONE";
                return render_to_response("web_interface/view_student_marks.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'root':root},context_instance = RequestContext(request))
        elif request.POST.get('tutB'):
            print "IN TUTB"
            module = request.POST.get('tutB')
            data ={
            'mod':module
            }
            result = views.viewSessionForMarker(request,json.dumps(data))
            res = json.loads(result.content)
            if res[0]['type'] == 1:
                assessments = res[0]['session']
                return render_to_response("web_interface/view_sessions_marker.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'assessmentName':assessments,
                                                                                'module':module,'type':1},
                                                                                context_instance = RequestContext(request))
            else:
                return render_to_response("web_interface/view_sessions_marker.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'type':-1},
                                                                                context_instance = RequestContext(request))
        elif request.POST.get('taB'):
            print "IN TAB"
            module = request.POST.get('taB')
            data ={
            'mod':module
            }         
            result = views.viewSessionForMarker(request,json.dumps(data))
            res = json.loads(result.content)
            if res[0]['type'] == 1:
                assessments = res[0]['session']
                return render_to_response("web_interface/view_sessions_marker.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'assessmentName':assessments,
                                                                                'module':module,'type':1},
                                                                                context_instance = RequestContext(request))
            else:
                return render_to_response("web_interface/view_sessions_marker.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'type':-1}
                                                                                ,context_instance = RequestContext(request))
        elif request.POST.get('lectB'):
            mod = request.POST['lectB']
            data ={
                'module':mod
            }
            result = views.testing(request,json.dumps(data))
            res = json.loads(result.content)
            print "-=-=-=-=-=-=-=-=--=-=-=-=-"+str(res)
            if res[0]['type'] == '1':
                print "something"
                root = res[0]['root']
                first = res[0]['first']
                second = res[0]['second']
                third = res[0]['third']
                return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'root':root,'first':first,
                                                                                'module':mod,'assessment':'',
                                                                                'second':second,'third':third},
                                                                                context_instance = RequestContext(request))
            else:
                print "NONE"
                root = "NONE";
                return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,
                                                                                'root':root},
                                                                                context_instance = RequestContext(request))
        else:
            raise Http404()

@isAuthenticated
def personDetails(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    if request.method == 'POST':
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
                                                                            'user_roles':user_roles,'name':name,'surname':surname,
                                                                            'title':title,'initials':initials},
                                                                            context_instance = RequestContext(request))
        else:
            return render_to_response("web_interface/person_details.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'user_roles':user_roles,'name':'person data not found'},
                                                                            context_instance = RequestContext(request))
    else:
        raise Http404()


@isAuthenticated
@isLecture
def getAllSessionsForAssessment(request):
    #try:
        user_type = ''
        # global default_user
        default_user =''
        #global user_roles
        user_roles = []
        #global user_lect
        user_lect = []
        # global user_stud
        user_stud = []
        #global user_tut
        user_tut = []
        #global user_ta
        user_ta = []
        user = request.session['user']
    
        if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
        if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
        if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
        if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
        #choosing the default user based on the user type ie,lecturer
        if len(user['lecturerOf']) != 0:
            default_user = 'LC'
        elif len(user['studentOf']) != 0:
            default_user = 'ST'
        elif len(user['tutorFor']) != 0:
            default_user = 'TT'
        else:
            default_user = 'TA'
    
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
                                                                            'user_roles':user_roles,
                                                                            'sessions':sessions,
                                                                            'assessmentName':assessmentName,
                                                                            'moduleName':moduleName,
                                                                            'assessment_id':assess,},
                                                                            context_instance = RequestContext(request))
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
                                                                            'user_roles':user_roles,'sessions':sessions,
                                                                            'assessment_id':assess,'assessmentName':assessmentName,
                                                                            'moduleName':moduleName},
                                                                            context_instance = RequestContext(request))
   # except Exception as e:
   #     raise Http404()

@isAuthenticated
@isLecture
def createSession(request):
    try:
        user_type = ''
        # global default_user
        default_user =''
        #global user_roles
        user_roles = []
        #global user_lect
        user_lect = []
        # global user_stud
        user_stud = []
        #global user_tut
        user_tut = []
        #global user_ta
        user_ta = []
        user = request.session['user']
    
        if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
        if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
        if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
        if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
        #choosing the default user based on the user type ie,lecturer
        if len(user['lecturerOf']) != 0:
            default_user = 'LC'
        elif len(user['studentOf']) != 0:
            default_user = 'ST'
        elif len(user['tutorFor']) != 0:
            default_user = 'TT'
        else:
            default_user = 'TA'
    
        print "huh gane y"
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
                                                                            'user_roles':user_roles,'sessions':sessions,'assessmentName':assess_name,
                                                                            'assessment_id':assess_id,
                                                                            'moduleName':mod,'SessionCreated':1},
                                                                            context_instance = RequestContext(request))
    
        else:
            assess_name = results[0]['assessmentName']
            sessions = results[0]['sessions']
            mod = results[0]['mod']
            return render_to_response("web_interface/create_sessions_lect.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'user_roles':user_roles,'sessions':sessions,'assessmentName':assess_name,
                                                                            'assessment_id':assess_id,
                                                                            'moduleName':mod,'SessionCreated':-1},
                                                                            context_instance = RequestContext(request))
    except Exception as e:
       raise Http404()
    
@isAuthenticated
@isLecture
def getAllStudentOfModule(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'

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
                                                                        'user_roles':user_roles,'students':students,'module':mod,
                                                                        'session_id':session,'tutor':tut,
                                                                        'teachingA':ta,'sessionName':name},
                                                                        context_instance = RequestContext(request))
    else:
        students = []
        ta = []
        tut = []
        name = res[0]['name']
        return render_to_response("web_interface/add_user_to_session.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'students':students,'module':mod,'session_id':session,
                                                                        'tutor':tut,'teachingA':ta,
                                                                        'sessionName':name},
                                                                        context_instance = RequestContext(request))

@isAuthenticated
@isLecture
def addStudentToSession(request):
    
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
        #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    mod = request.POST['module']
    session_id = request.POST['session']
    users = request.POST.lists()
    print "]]]]]]]]]]]]]]]]]] huh wena wa hlanya shem"
    print users
    print "Part : " + str(users[0][1])
    print "len(user[0][1]) = " + str(len(users[0][1]))
    print "users[5][1] = " + str(users[5][1])
    Studentarray = []
    MarkerArray = []
    if (users[0][0] == 'userS' and (len(users[0][1]) >= 1 and str(users[0][1][0]) != "None")): #Apparently, if something has an empty string, it is counted, thus 1 and not 0 (zero)
        print "Students : " + str(users[0][1])
        for n in users[0][1]:
            Studentarray.append(n)
    else:
        print "Markers : " + str(users[0][1])
        for n in users[5][1]:
            MarkerArray.append(n)
    print "studnt array"+ str(Studentarray)
    data = {
        'student':Studentarray,
        'marker':MarkerArray,
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
                                                                        'sessionName':name,'marker':marker,'studentAdded':1},
                                                                        context_instance = RequestContext(request))
    else:
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
                                                                        'sessionName':name,'marker':marker,'studentAdded':-1},
                                                                        context_instance = RequestContext(request))

@isAuthenticated
@isLecture
def getAllPersonOfSession(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
        #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    mod = request.POST['module']
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
                                                                        'sessionName':sessionName,'marker':marker},
                                                                        context_instance = RequestContext(request))
    else:
        return render_to_response("web_interface/added_user_to_session.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'students':[],
                                                                        'module':mod,'session_id':session_id,
                                                                        'sessionName':'An error occurred, a session was not found!',
                                                                        'marker':[]},context_instance = RequestContext(request))

@isAuthenticated
@isLecture
def getLeafAssessmentPage(request):
    
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    assess_id = request.POST['assessment']
    mod = request.POST['module']
    
    data = {
        'assess_id':assess_id,
        'mod':mod
    }
    results = views.getAllChildrenOfAssessment(request,json.dumps(data))
    res = json.loads(results.content)
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
                                                                        'module':mod,'assessmentName':name,'assess_id':assess_id,
                                                                        'fullmark':fullmark,'type':-1},context_instance = RequestContext(request))


@isAuthenticated
@isLecture
def createLeafAssessment(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    assessName = request.POST['name']
    mod = request.POST['module']
    fullmark = request.POST['fullmark']
    assess_id = request.POST['assess_id']
    
    data = {
        'name':assessName,
        'mod':mod,
        'fullmark':fullmark,
        'assess_id': assess_id
    }
    results= views.createLeafAssessment(request,json.dumps(data))
    res = json.loads(results.content)
    if res[0]['type'] == 1:
        print "something"
        root = res[0]['root']
        first = res[0]['first']
        second = res[0]['second']
        third = res[0]['third']
        return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'root':root,'first':first,
                                                                        'module':mod,'second':second,'AssessCreated':1,
                                                                        'third':third},context_instance = RequestContext(request))
    else:
        print "NONE"
        root = "NONE";
        return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'AssessCreated':-1,
                                                                        'user_roles':user_roles,'root':root},context_instance = RequestContext(request))


@isAuthenticated
@isLecture
def updateMarkForStudent(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    leaf_id = request.POST['assess_id']
    mark = request.POST['mark']
    student = request.POST['uid']
    mod = request.POST['module']
    comment = request.POST['reason']
    print "i ma a lecture"
    data = {
        'leaf_id':leaf_id,
        'mark':mark,
        'student':student,
        'mod':mod,
        'reason':comment
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
                                                                        'module':mod,'assessmentName':name,'assess_id':leaf_id,
                                                                        'fullmark':fullmark,'message':1},context_instance = RequestContext(request))
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
                                                                        'module':mod,'assessmentName':name,'assess_id':leaf_id,'fullmark':fullmark,
                                                                        'message':0},context_instance = RequestContext(request))


@isAuthenticated
@isLecture
def deleteAssessment(request):
    #try:
        user_type = ''
        # global default_user
        default_user =''
        #global user_roles
        user_roles = []
        #global user_lect
        user_lect = []
        # global user_stud
        user_stud = []
        #global user_tut
        user_tut = []
        #global user_ta
        user_ta = []
        user = request.session['user']
    
        if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
        if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
        if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
        if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
        #choosing the default user based on the user type ie,lecturer
        if len(user['lecturerOf']) != 0:
            default_user = 'LC'
        elif len(user['studentOf']) != 0:
            default_user = 'ST'
        elif len(user['tutorFor']) != 0:
            default_user = 'TT'
        else:
            default_user = 'TA'
    
        assess_id = request.POST['assess_id']
        mod = request.POST['module']
        
        data = {
            'assess_id':assess_id,
        }
        result = views.deleteAssessment(request,json.dumps(data))
        res = json.loads(result.content)
        
        if res[0]['type'] == 1:
            data ={
                    'module':mod
                }
            results = views.testing(request,json.dumps(data))
            res = json.loads(results.content)
            print "-=-=-=-=-=-=-=-=--=-=-=-=-"+str(res)
            if res[0]['type'] == '1':
                print "something"
                root = res[0]['root']
                first = res[0]['first']
                second = res[0]['second']
                third = res[0]['third']
                return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'root':root,'first':first,
                                                                                'module':mod,'assessment':'',
                                                                                'second':second,'third':third,"AssessDeleted":1},
                                                                                context_instance = RequestContext(request))
            else:
                print "NONE"
                root = "NONE";
                return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,"AssessDeleted":-1,'root':root},
                                                                                context_instance = RequestContext(request))
    #except Exception as e:
    #    raise Http404()

@isAuthenticated
@isLecture
def deleteSession(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    sess_id = request.POST['session']
    assess_id = request.POST['assessment']
    mod = request.POST['module']
    
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
                                                                            'user_roles':user_roles,'sessions':sessions,
                                                                            'assessmentName':assessmentName,
                                                                            'moduleName':moduleName,
                                                                            'assessment_id':assess_id,
                                                                            'message':1},context_instance = RequestContext(request))
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
                                                                            'user_roles':user_roles,'sessions':sessions,
                                                                            'assessment_id':assess_id,
                                                                            'assessmentName':assessmentName,
                                                                            'moduleName':moduleName,'message':1},
                                                                            context_instance = RequestContext(request))
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
                                                                            'user_roles':user_roles,'sessions':sessions,'assessmentName':assessmentName,
                                                                            'moduleName':moduleName,'assessment_id':assess_id,
                                                                            'message':0},context_instance = RequestContext(request))
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
                                                                            'user_roles':user_roles,'sessions':sessions,
                                                                            'assessment_id':assess_id,
                                                                            'assessmentName':assessmentName,
                                                                            'moduleName':moduleName,'message':0},
                                                                            context_instance = RequestContext(request))

@isAuthenticated
@isLecture
def changeAssessmentFullMark(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    assess_id = request.POST['assess_id']
    mod = request.POST['module']
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
                                                                                'module':mod,'assessmentName':name,
                                                                                'assess_id':assess_id,'fullmark':fullmark,'mark_update_response':1},
                                                                                context_instance = RequestContext(request))
    else:
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
                                                                                'module':mod,'assessmentName':name,
                                                                                'assess_id':assess_id,'fullmark':fullmark,"mark_update_response":-1},
                                                                                context_instance = RequestContext(request))

def changeLeafAssessmentName(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    assess_id = request.POST['assess_id']
    module = request.POST['module']
    name = request.POST['assess_name']
    
    data ={
        "assess_id":assess_id,
        "name":name
    }
    
    results = views.changeLeafAssessmentName(request,json.dumps(data))
    res = json.loads(results.content)
    if res[0]['type']:
        data ={
        'assess_id':assess_id,
        }
        result = views.assessmentCenterLeaf(request,json.dumps(data))
        res = json.loads(result.content)
        if res['type'] ==1:
            assessmentName = res['assessmentName']
            average = res['average']
            median = res['median']
            mode = res['mode']
            frequency = res['frequency']
            stddev = res['stddev']
            studentlist = res['students']
            pass_fail_percentage = res['pass_fail_percentage']

            return render_to_response("web_interface/leaf_assessment_center.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,
                                                                        'average':average,'median':median,'mode':mode,'frequency':frequency,
                                                                        'stddev':stddev,'studentlist':studentlist,
                                                                        'assess_id':assess_id,'assessmentName':assessmentName,
                                                                        'module':module,"AssessName":1, 'pass_fail_percentage':pass_fail_percentage}, context_instance=RequestContext(request))

        else:
            return render_to_response("web_interface/leaf_assessment_center.htm",{'default_user':default_user,
                                                                'user_lect':user_lect,
                                                                'user_stud':user_stud,
                                                                'user_tut':user_tut,
                                                                'user_ta':user_ta,
                                                                'user_roles':user_roles,'agg_name':agg_name, 'numChildren':numChildren,'message':message,
                                                                'children':children,"AssessName":1 ,'assess_id':assess_id,'assessmentName':assessmentName, 'module':module}, context_instance=RequestContext(request))
    else:
        data ={
        'assess_id':assess_id,
        }
        result = views.assessmentCenterLeaf(request,json.dumps(data))
        res = json.loads(result.content)
        if res['type'] ==1:
            assessmentName = res['assessmentName']
            average = res['average']
            median = res['median']
            mode = res['mode']
            frequency = res['frequency']
            stddev = res['stddev']
            studentlist = res['students']
            pass_fail_percentage = res['pass_fail_percentage']

            return render_to_response("web_interface/leaf_assessment_center.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,
                                                                        'average':average,'median':median,'mode':mode,'frequency':frequency,
                                                                        'stddev':stddev,'studentlist':studentlist,
                                                                        'assess_id':assess_id,'assessmentName':assessmentName,
                                                                        'module':module,"AssessName":-1, 'pass_fail_percentage':pass_fail_percentage}, context_instance=RequestContext(request))

        else:
            return render_to_response("web_interface/leaf_assessment_center.htm",{'default_user':default_user,
                                                                'user_lect':user_lect,
                                                                'user_stud':user_stud,
                                                                'user_tut':user_tut,
                                                                'user_ta':user_ta,
                                                                'user_roles':user_roles,'agg_name':agg_name, 'numChildren':numChildren,'message':message,
                                                                'children':children, "AssessName":-1,'assess_id':assess_id,'assessmentName':assessmentName, 'module':module}, context_instance=RequestContext(request))

#@isAuthenticated
#@isLecture
def changeAssessmentName(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    assess_id = request.POST['assess_id']
    module = request.POST['module']
    name = request.POST['assess_name']
    
    data = {
        'assess_id':assess_id,
        'assess_name':name
    }
    result = views.changeAssessmentName(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] == 1:
        data={
                'assess_id':assess_id
        }
        result = views.assessmentCenter(request,json.dumps(data))
        res = json.loads(result.content)
        if res['type'] ==1:

	    numChildren = res['numChildren']
	    children = res['children']
	    assessmentName = res['assessmentName']
	    agg_name = res['agg_name']
	    average = res['average']
	    median = res['median']
	    mode = res['mode']
	    frequency = res['frequency']
	    stddev = res['stddev']
	    studentlist = res['students']
	    pass_fail_percentage = res['pass_fail_percentage']

	    return render_to_response("web_interface/assessment_center.htm",{'default_user':default_user,
	    	    	    	    	    	    	    	    	'user_lect':user_lect,
	    	    	    	    	    	    	    	    	'user_stud':user_stud,
	    	    	    	    	    	    	    	    	'user_tut':user_tut,
	    	    	    	    	    	    	    	    	'user_ta':user_ta,
	    	    	    	    	    	    	    	    	'user_roles':user_roles,'agg_name':agg_name, 'numChildren':numChildren,
	    	    	    	    	    	    	    	    	'average':average,'median':median,'mode':mode,'frequency':frequency,
	    	    	    	    	    	    	    	    	'stddev':stddev,'studentlist':studentlist,
	    	    	    	    	    	    	    	    	'children':children, 'assess_id':assess_id,'assessmentName':assessmentName,
	    	    	    	    	    	    	    	    	'module':module, 'pass_fail_percentage':pass_fail_percentage}, context_instance=RequestContext(request))

	else:
	    numChildren = res['numChildren']
	    children = res['children']
	    assessmentName = res['assessmentName']
	    agg_name = res['agg_name']
	    average = res['average']
	    median = res['median']
	    mode = res['mode']
	    frequency = res['frequency']
	    stddev = res['stddev']
	    studentlist = res['students']
	    pass_fail_percentage = res['pass_fail_percentage']

	    return render_to_response("web_interface/assessment_center.htm",{'default_user':default_user,
	    	    	    	    	    	    	    	    	'user_lect':user_lect,
	    	    	    	    	    	    	    	    	'user_stud':user_stud,
	    	    	    	    	    	    	    	    	'user_tut':user_tut,
	    	    	    	    	    	    	    	    	'user_ta':user_ta,
	    	    	    	    	    	    	    	    	'user_roles':user_roles,'agg_name':agg_name, 'numChildren':numChildren,
	    	    	    	    	    	    	    	    	'average':average,'median':median,'mode':mode,'frequency':frequency,
	    	    	    	    	    	    	    	    	'stddev':stddev,'studentlist':studentlist,
	    	    	    	    	    	    	    	    	'children':children, 'assess_id':assess_id,'assessmentName':assessmentName,
	    	    	    	    	    	    	    	    	'module':module, 'pass_fail_percentage':pass_fail_percentage}, context_instance=RequestContext(request))
    else:
        numChildren = res['numChildren']
        children = res['children']
        assessmentName = res['assessmentName']
        agg_name = res['agg_name']
        average = res['average']
        median = res['median']
        mode = res['mode']
        frequency = res['frequency']
        stddev = res['stddev']
        studentlist = res['students']
        pass_fail_percentage = res['pass_fail_percentage']

        return render_to_response("web_interface/assessment_center.htm",{'default_user':default_user,
                                                                    'user_lect':user_lect,
                                                                    'user_stud':user_stud,
                                                                    'user_tut':user_tut,
                                                                    'user_ta':user_ta,
                                                                    'user_roles':user_roles,'agg_name':agg_name, 'numChildren':numChildren,
                                                                    'average':average,'median':median,'mode':mode,'frequency':frequency,
                                                                    'stddev':stddev,'studentlist':studentlist,
                                                                    'children':children, 'assess_id':assess_id,'assessmentName':assessmentName,
                                                                    'module':module, 'pass_fail_percentage':pass_fail_percentage}, context_instance=RequestContext(request))


@isAuthenticated
@isLecture
def setPublishedStatus(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    assess_id = request.POST['assess_id']
    status = request.POST['publish_state'] #whether assessment is published(1) or not(0)
    mod_code = request.POST['module']
    
    
    data = {
        'assess_id':assess_id,
        'status':status,
        'module':mod_code
    }
    print "B5 RESULTANT>>>"
    result = views.setPublishedStatus(request,json.dumps(data))
    res = json.loads(result.content)
    print "AFTER PARTY TIME!!!"

    if res[0]['type'] == 1:
            data ={
                'module':mod_code
            }
            result = views.testing(request,json.dumps(data))
            res = json.loads(result.content)
            print "-=-=-=-=-=-=-=-=--=-=-=-=-"+str(res)
            if res[0]['type'] == '1':
                print "something"
                root = res[0]['root']
                first = res[0]['first']
                second = res[0]['second']
                third = res[0]['third']
                return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'root':root,'first':first,
                                                                                'module':mod_code,'assessment':'','second':second,"published":1,
                                                                                'third':third},context_instance = RequestContext(request))
            else:
                print "NONE"
                root = "NONE";
                return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,"published":1,'root':root},
                                                                                context_instance = RequestContext(request))
    else:
            data ={
                'module':mod_code
            }
            result = views.testing(request,json.dumps(data))
            res = json.loads(result.content)
            print "-=-=-=-=-=-=-=-=--=-=-=-=-"+str(res)
            if res[0]['type'] == '1':
                print "something"
                root = res[0]['root']
                first = res[0]['first']
                second = res[0]['second']
                third = res[0]['third']
                return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'root':root,'first':first,
                                                                                'module':mod_code,'assessment':'',
                                                                                'second':second,'third':third,"published":-1},
                                                                                context_instance = RequestContext(request))
            else:
                print "NONE"
                root = "NONE";
                return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'root':root,"published":-1},
                                                                                context_instance = RequestContext(request))


@isAuthenticated
@isLecture
def setPublishedStatusInLeaf(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    assess_id = request.POST['assess_id']
    status = request.POST['publish_state'] #whether assessment is published(1) or not(0)
    mod_code = request.POST['mod']
    
    
    data = {
        'assess_id':assess_id,
        'status':status,
        'module':mod_code
    }
    data_mod = {
        'mod':mod_code,
        'assess_id':assess_id
    }
    print "B5 RESULTANT>>>"
    result = views.setPublishedStatus(request,json.dumps(data))
    relo = views.getAllChildrenOfAssessmentForLeaf(request,json.dumps(data_mod))
    res = json.loads(result.content)
    res_mod = json.loads(relo.content)
    print "AFTER PARTY TIME!!!"
    
    if res_mod[0]['type'] == 1:
        if res_mod[0]['message'] == 'Aggregate':
            child = res_mod[0]['child']
            name = res_mod[0]['name']
            return render_to_response("web_interface/view_aggregate_assessments.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'child':child,
                                                                        'module':mod_code,'assessmentName':name,
                                                                        'assess_id':assess_id,'type':1},
                                                                        context_instance = RequestContext(request))
        
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
                                                                        'module':mod_code,'assessmentName':name,'assess_id':assess_id,
                                                                        'fullmark':fullmark,'type':-1},
                                                                        context_instance = RequestContext(request))

@isAuthenticated
@isPartOfmodule
def viewAssessment(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    module = ""
    if request.POST.get('studB'):
        module = request.POST['studB']
        data ={
                'module':module
            }
        result = views.testingStudentAssessmentForModule(request,json.dumps(data))
        res = json.loads(result.content)
        print "-=-=-=-=-=-=-=-=--=-=-=-=-"+str(res)
        if res[0]['type'] == '1':
            print "something"
            root = res[0]['root']
            first = res[0]['first']
            second = res[0]['second']
            third = res[0]['third']
            return render_to_response("web_interface/view_student_marks.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'root':root,'first':first,
                                                                                'module':module,'second':second,'third':third,},context_instance = RequestContext(request))
        else:
            print "NONE"
            root = "NONE";
            return render_to_response("web_interface/view_student_marks.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'root':root},context_instance = RequestContext(request))
    elif request.POST.get('lectB'):
        module = request.POST['lectB']
        data = {'module': module}
        result = views.testing(request,json.dumps(data))
        res = json.loads(result.content)
        print "-=-=-=-=-=-=-=-=--=-=-=-=-"+str(res)
        if res[0]['type'] == '1':
            print "something"
            root = res[0]['root']
            print "ROOT : " + str(root)
            first = res[0]['first']
            print "FIRST : " + str(first)
            second = res[0]['second']
            print "SECOND : " + str(second)
            third = res[0]['third']
            print "THIRD : " + str(third)
            return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'root':root,'first':first,
                                                                                'module':module,'assessment':'',
                                                                                'second':second,'third':third},
                                                                                context_instance = RequestContext(request))
        else:
            print "NONE"
            root = "NONE";
            return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,
                                                                                'root':root},
                                                                                context_instance = RequestContext(request))
    elif request.POST.get('tutB'):
        module = request.POST['tutB']
        data ={
            'mod':module
            }
        result = views.viewSessionForMarker(request,json.dumps(data))
        res = json.loads(result.content)
        if res[0]['type'] == 1:
            assessments = res[0]['session']
            return render_to_response("web_interface/view_sessions_marker.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'assessmentName':assessments,
                                                                                'module':module,'type':1},
                                                                                context_instance = RequestContext(request))
        else:
            return render_to_response("web_interface/view_sessions_marker.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'type':-1},
                                                                                context_instance = RequestContext(request))
    elif request.POST.get('taB'):
        module = request.POST['taB']
        data ={
            'mod':module
            }
        result = views.viewSessionForMarker(request,json.dumps(data))
        res = json.loads(result.content)
        if res[0]['type'] == 1:
            assessments = res[0]['session']
            return render_to_response("web_interface/view_sessions_marker.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'assessmentName':assessments,
                                                                                'module':module,'type':1},
                                                                                context_instance = RequestContext(request))
        else:
            return render_to_response("web_interface/view_sessions_marker.htm",{'default_user':default_user,
                                                                                'user_lect':user_lect,
                                                                                'user_stud':user_stud,
                                                                                'user_tut':user_tut,
                                                                                'user_ta':user_ta,
                                                                                'user_roles':user_roles,'type':-1},
                                                                                context_instance = RequestContext(request))
    else:
        del request.session['user']
        return HttpResponseRedirect(reverse('home'))
    
    

@isAuthenticated
@isLecture
def openOrCloseSession(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    assess_id = request.POST['assess_id']
    sess_id = request.POST['sess_id']
    status = request.POST['status'] #whether to open or close it 0: closeSession 1:openSession
    
    data = {
        'assess_id':assess_id,
        'sess_id':sess_id,
        'status':status
    }
    print "B4 RESULT>>>"
    result = views.openOrCloseSession(request,json.dumps(data))
    res = json.loads(result.content)
    print "AFTER PARTY!!!"
    
    if res[0]['type'] == 1:
        message = res[0]['message']
        data = {
            'assessmentID':assess_id
        }
        session = views.getAllSessionsForAssessment(request,json.dumps(data))
        sess = json.loads(session.content)
        sessions = []
        if sess[0]['type'] == 1:
            sessions = sess[0]['sessions']
            assessmentName = sess[0]['assessmentName']
            moduleName=sess[0]['moduleName']
            return render_to_response("web_interface/create_sessions_lect.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'user_roles':user_roles,
                                                                            'sessions':sessions,
                                                                            'assessmentName':assessmentName,
                                                                            'moduleName':moduleName,
                                                                            'assessment_id':assess_id,'type':1},
                                                                            context_instance = RequestContext(request))
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
                                                                            'user_roles':user_roles,'sessions':sessions,
                                                                            'assessment_id':assess_id,'assessmentName':assessmentName,
                                                                            'moduleName':moduleName,'type':1},
                                                                            context_instance = RequestContext(request))
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
            moduleName=sess[0]['moduleName']
            return render_to_response("web_interface/create_sessions_lect.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'user_roles':user_roles,
                                                                            'sessions':sessions,
                                                                            'assessmentName':assessmentName,
                                                                            'moduleName':moduleName,
                                                                            'assessment_id':assess_id,'type':-1},
                                                                            context_instance = RequestContext(request))
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
                                                                            'user_roles':user_roles,'sessions':sessions,'assessment_id':assess_id,
                                                                            'assessmentName':assessmentName,'moduleName':moduleName,
                                                                            'type':-1},context_instance = RequestContext(request))


#marker view
@isAuthenticated
def viewChildrenOfAssessments(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
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
                                                                        'module':mod,'assessmentName':name,
                                                                        'assess_id':assess_id},
                                                                        context_instance=RequestContext(request))
        
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
                                                                        'module':mod,'assessmentName':name,
                                                                        'assess_id':assess_id,'fullmark':fullmark}
                                                                        ,context_instance=RequestContext(request))

@isAuthenticated
def viewSessionForMarker(request):
    mod = request.POST['studB']
    
    data ={
        'mod':mod
    }
    result = views.viewSessionForMarker(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] == 1:
        assessments = res[0]['session']
        return render_to_response("web_interface/view_session.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':assessments,
                                                                        'module':mod,'type':1},context_instance=RequestContext(request))
    else:
        return render_to_response("web_interface/view_session.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'user_roles':user_roles,'type':-1},context_instance=RequestContext(request))


@isAuthenticated
def viewAssessmentForMarker(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    mod = request.POST['mod']
    assessment = request.POST['session']
    
    data = {
        'sessions':assessment
    }
    results = views.viewAssessmentForMarker(request,json.dumps(data))
    res = json.loads(results.content)
    if res[0]['type'] == 1:
        assessment = res[0]['assessment']
        session = res[0]['session']
        return render_to_response("web_interface/view_assessments_marker.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'user_roles':user_roles,'module':mod,
                                                                       'session':session,'assessmentName':assessment,
                                                                       'type':1},context_instance=RequestContext(request))
    else:
        session = res[0]['session']
        return render_to_response("web_interface/view_assessments_marker.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'user_roles':user_roles,'module':mod,
                                                                       'session':session,'type':-1},context_instance=RequestContext(request))

@isAuthenticated
def viewStudentsForAssessment(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    sess= request.POST['session']
    assess = request.POST['assessment']
    mod = request.POST['mod']
    print "am fine"
    data = {
        'session':sess,
        'assess_id':assess
    }
    results = views.viewStudentsForAssessment(request,json.dumps(data))
    res = json.loads(results.content)
    if res[0]['type'] == 1:
        assessment = res[0]['assessment']
        fullmark = res[0]['fullmark']
        students = res[0]['students']
        return render_to_response("web_interface/view_leaf_marker.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'studentMark':students,
                                                                        'module':mod,'assessmentName':assessment,
                                                                        'session':sess,'assess_id':assess,
                                                                        'fullmark':fullmark},context_instance=RequestContext(request))
    else:
        students = []
        return render_to_response("web_interface/success.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessment':assessment,'students':student,
                                                                        'fullmark':fullmark,'module':mod},
                                                                        context_instance=RequestContext(request))

@isAuthenticated
@isMarker
def updateMarkForStudentMarker(request):
    
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    session = request.POST['session']
    leaf_id = request.POST['assess_id']
    mark = request.POST['mark']
    student = request.POST['uid']
    mod = request.POST['module']
    comment = request.POST['reason']
    print "am a marker"
    data = {
        'leaf_id':leaf_id,
        'mark':mark,
        'student':student,
        'mod':mod,
        'session':session,
        'reason':comment
    }
    
    result = views.updateMarkForStudentMarker(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] == 1:
        studentMark = res[0]['studentMark']
        name = res[0]['name']
        fullmark = res[0]['fullmark']
        return render_to_response("web_interface/view_leaf_marker.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'studentMark':studentMark,
                                                                        'module':mod,'assessmentName':name,
                                                                        'assess_id':leaf_id,'fullmark':fullmark,
                                                                        'session':session,'message':1},
                                                                        context_instance=RequestContext(request))
    else:
        studentMark = res[0]['studentMark']
        name = res[0]['name']
        fullmark = res[0]['fullmark']
        return render_to_response("web_interface/view_leaf_marker.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'studentMark':studentMark,
                                                                        'module':mod,'assessmentName':name,'assess_id':leaf_id,
                                                                        'fullmark':fullmark,'session':session,
                                                                        'message':0},context_instance=RequestContext(request))



##################################### STUDENT VIEWS #############################################################################
#student views
@isAuthenticated
@isStudent
def viewAssessmentsForStudent(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    mod = request.POST['studB']
    uid = request.session['user']['uid'][0]
    
    data = {
        'mod_code':mod,
        'uid': uid
    }
    data = views.viewStudentAssessment(request, json.dumps(data))
    result = json.loads(data.content)
    assessmentName = []
    assessmentId = []
    if result[0]['type'] == 1:
        person = result[0]['person']
        assessmentName = 'Base Assessments Page'
        assessments = result[0]['assessments']
        return render_to_response("web_interface/view_student_marks_agg.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles, 'assessments':assessments,
                                                                        'module':mod,'type':1, 'assessmentName':person},context_instance=RequestContext(request))
    else:
        assessmentName = "There Are No Assessments."
        assessmentId = 0
        #person = result[0]['person']
        return render_to_response("web_interface/view_student_marks_agg.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assessmentName':'ERROR',
                                                                        'assessmentId':assessmentId,'module':mod,
                                                                        'type':-1},context_instance=RequestContext(request))

@isAuthenticated
@isStudent
def getAllChildrenOfAssessmentForStudent(request):
        user_type = ''
        default_user =''
        user_roles = []
        user_lect = []
        user_stud = []
        user_tut = []
        user_ta = []
        user = request.session['user']
    
        if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
        if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
        if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
        if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
        #choosing the default user based on the user type ie,lecturer
        if len(user['lecturerOf']) != 0:
            default_user = 'LC'
        elif len(user['studentOf']) != 0:
            default_user = 'ST'
        elif len(user['tutorFor']) != 0:
             default_user = 'TT'
        else:
            default_user = 'TA'
    
        mod = request.POST['module']
        assessment = request.POST['assess_id']
        data ={
            'assess_id':assessment
        }
        result = views.testingStudentAssessment(request,json.dumps(data))
        res = json.loads(result.content)
        print "-=-=-=-=-=-=-=-=--=-=-=-=-"+str(res)
        if res[0]['type'] == '1':
            print "something"
            root = res[0]['root']
            print "root: " + str(root)
            first = res[0]['first']
            print "first: " + str(first)
            second = res[0]['second']
            print "second: " + str(second)
            third = res[0]['third']
            print "third: "+ str(third)
            name = res[0]['assess_name']
            return render_to_response("web_interface/view_student_marks.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'user_roles':user_roles,'root':root,'first':first,
                                                                            'module':mod, 'assessment':name,'second':second,'third':third,'assessmentName':assessment})
        else:
            print "NONE"
            root = "NONE";
            return render_to_response("web_interface/view_student_marks.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'user_roles':user_roles,'root':root})


################################################ END STUDENT VIEWS ################################################################
@isAuthenticated
@isLecture
def getAllAssessmentOfAssessment(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    mod = request.POST['mod']
    assessment = request.POST['assessment']
    data ={
        'assess_id':assessment
    }
    result = views.testingAssessment(request,json.dumps(data))
    res = json.loads(result.content)
    print "-=-=-=-=-=-=-=-=--=-=-=-=-"+str(res)
    if res[0]['type'] == '1':
        print "something"
        root = res[0]['root']
        first = res[0]['first']
        second = res[0]['second']
        third = res[0]['third']
        name = res[0]['assess_name']
        return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'root':root,'first':first,
                                                                        'module':mod, 'assessment':name,
                                                                        'second':second,'third':third,
                                                                        'assessmentName':assessment},
                                                                        context_instance=RequestContext(request))
    else:
        print "NONE"
        root = "NONE";
        return render_to_response("web_interface/testing.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'root':root},
                                                                        context_instance=RequestContext(request))

@isAuthenticated
@isLecture
def ChangeSessionTime(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    mod = request.POST['module']
    session = request.POST['session']
    assess=request.POST['assess']
    opn = request.POST['open']
    close = request.POST['close']
    
    data = {
        'session': session,
        'open':opn,
        'close':close
    }
    
    results = views.ChangeSessionTime(request,json.dumps(data))
    res = json.loads(results.content)
    if res[0]['type'] == 1:
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
                                                                            'user_roles':user_roles,
                                                                            'sessions':sessions,
                                                                            'assessmentName':assessmentName,
                                                                            'moduleName':moduleName,
                                                                            'assessment_id':assess,})
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

@isAuthenticated
@isLecture
def removeUserfromSession(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    mod = request.POST['module']
    session_id = request.POST['session']
    users = request.POST.lists()
    print "]]]]]]]]]]]]]]]]]] huh wena wa hlanya shem"
    #print users
    # users[1][1][0]
    Studentarray = []
    MarkerArray = []
    if (users[0][0] == 'userS' and (len(users[0][1]) >= 1) and str(users[0][1][0]) != "None" ): #Apparently, if something has an empty string, it is counted, thus 1 and not 0 (zero)
        print "Students : " + str(users[0][1])
        for n in users[0][1]:
            Studentarray.append(n)
    else:
        print "Markers : " + str(users[0][1])
        for n in users[5][1]:
            MarkerArray.append(n)
    print "studnt array"+ str(Studentarray)
    data = {
        'student':Studentarray,
        'marker':MarkerArray,
        'session':session_id	
    }
    results = views.removeUserfromSession(request,json.dumps(data))
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
                                                                        'sessionName':name,'marker':marker,"studentRemoved":1},context_instance=RequestContext(request))
    else:
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
                                                                        'sessionName':name,'marker':marker,"studentRemoved":-1},context_instance=RequestContext(request))

@isAuthenticated
def AuditLog(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    start = request.POST['search_from']
    finish=request.POST['search_till']
    data = {
        'start':start,
        'end':finish
    }
    result = views.Auditlog(request,json.dumps(data))
    res = json.loads(result.content)
    assess = res[0]['Assessment']
    session=res[0]['Session']
    markAlloc= res[0]['markAllocation']
    allocate = res[0]['allocatePerson']
    
    return render_to_response("web_interface/audit_table.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'assess':assess,
                                                                        'session':session,'markAlloc':markAlloc,
                                                                        'allocate':allocate},context_instance=RequestContext(request))
    
'''
###################### Aggregation Views ####################################
'''
@isAuthenticated
@isLecture
def assessmentCenterLeaf(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    assess_id = request.POST['assess_id']
    module = request.POST['module']
    data ={
        'assess_id':assess_id,
    }
    result = views.assessmentCenterLeaf(request,json.dumps(data))
    res = json.loads(result.content)
    if res['type'] ==1:
        assessmentName = res['assessmentName']
        average = res['average']
        median = res['median']
        mode = res['mode']
        frequency = res['frequency']
        stddev = res['stddev']
        studentlist = res['students']
        pass_fail_percentage = res['pass_fail_percentage']

        return render_to_response("web_interface/leaf_assessment_center.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,
                                                                        'average':average,'median':median,'mode':mode,'frequency':frequency,
                                                                        'stddev':stddev,'studentlist':studentlist,
                                                                        'assess_id':assess_id,'assessmentName':assessmentName,
                                                                        'module':module, 'pass_fail_percentage':pass_fail_percentage}, context_instance=RequestContext(request))

    else:
        assessmentName = res['assessmentName']
        return render_to_response("web_interface/leaf_assessment_center.htm",{'default_user':default_user,
                                                                'user_lect':user_lect,
                                                                'user_stud':user_stud,
                                                                'user_tut':user_tut,
                                                                'user_ta':user_ta,
                                                                'user_roles':user_roles,
                                                                'assess_id':assess_id,'assessmentName':assessmentName, 'module':module}, context_instance=RequestContext(request))

@isAuthenticated
@isLecture
def assessmentCenter(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    assess_id = request.POST['assess_id']
    module = request.POST['module']
    data ={
        'assess_id':assess_id,
    }
    result = views.assessmentCenter(request,json.dumps(data))
    res = json.loads(result.content)
    if res['type'] ==1:
        numChildren = res['numChildren']
        children = res['children']
        assessmentName = res['assessmentName']
        agg_name = res['agg_name']
        average = res['average']
        median = res['median']
        mode = res['mode']
        frequency = res['frequency']
        stddev = res['stddev']
        studentlist = res['students']
        pass_fail_percentage = res['pass_fail_percentage']

        return render_to_response("web_interface/assessment_center.htm",{'default_user':default_user,
                                                                        'user_lect':user_lect,
                                                                        'user_stud':user_stud,
                                                                        'user_tut':user_tut,
                                                                        'user_ta':user_ta,
                                                                        'user_roles':user_roles,'agg_name':agg_name, 'numChildren':numChildren,
                                                                        'average':average,'median':median,'mode':mode,'frequency':frequency,
                                                                        'stddev':stddev,'studentlist':studentlist,
                                                                        'children':children, 'assess_id':assess_id,'assessmentName':assessmentName,
                                                                        'module':module, 'pass_fail_percentage':pass_fail_percentage}, context_instance=RequestContext(request))

    else:
        numChildren = res['numChildren']
        children = res['children']
        assessmentName = res['assessmentName']
        agg_name = res['agg_name']
        average = res['average']
        median = res['median']
        mode = res['mode']
        frequency = res['frequency']
        stddev = res['stddev']
        studentlist = res['students']
        pass_fail_percentage = res['pass_fail_percentage']
        return render_to_response("web_interface/assessment_center.htm",{'default_user':default_user,
                                                                'user_lect':user_lect,
                                                                'user_stud':user_stud,
                                                                'user_tut':user_tut,
                                                                'user_ta':user_ta,
                                                                'user_roles':user_roles,'agg_name':agg_name, 'numChildren':numChildren,
                                                                'children':children, 'assess_id':assess_id,'assessmentName':assessmentName, 'module':module}, context_instance=RequestContext(request))
 
@isAuthenticated
@isLecture
def aggregateMarkForAssessment(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    agg_name = request.POST['agg_name']
    numContributors = request.POST['numC']
    
    #Converting QueryDict to python dict
    myDict = dict(request.POST.iterlists())
    
    child_weight = myDict['child_weight']
    child_id = myDict['child_id']
    
    assess_id = request.POST['assess_id']
    module = request.POST['module']
    
    data = {
        'assess_id':assess_id,
        'agg_name':agg_name,
        'numContributors':numContributors,
        'module':module,
        'child_weight':child_weight,
        'child_id':child_id
    }

    result = views.aggregateMarkForAssessment(request,json.dumps(data))
    res = json.loads(result.content)


    if res['type'] ==1:

	    numChildren = res['numChildren']
	    children = res['children']
	    assessmentName = res['assessmentName']
	    agg_name = res['agg_name']
	    average = res['average']
	    median = res['median']
	    mode = res['mode']
	    frequency = res['frequency']
	    stddev = res['stddev']
	    studentlist = res['students']
	    pass_fail_percentage = res['pass_fail_percentage']

	    return render_to_response("web_interface/assessment_center.htm",{'default_user':default_user,
	    	    	    	    	    	    	    	    	'user_lect':user_lect,
	    	    	    	    	    	    	    	    	'user_stud':user_stud,
	    	    	    	    	    	    	    	    	'user_tut':user_tut,
	    	    	    	    	    	    	    	    	'user_ta':user_ta,
	    	    	    	    	    	    	    	    	'user_roles':user_roles,'agg_name':agg_name, 'numChildren':numChildren,
	    	    	    	    	    	    	    	    	'average':average,'median':median,'mode':mode,'frequency':frequency,
	    	    	    	    	    	    	    	    	'stddev':stddev,'studentlist':studentlist,
	    	    	    	    	    	    	    	    	'children':children, 'assess_id':assess_id,'assessmentName':assessmentName,
	    	    	    	    	    	    	    	    	'module':module, 'pass_fail_percentage':pass_fail_percentage}, context_instance=RequestContext(request))


'''
###################### End Aggregation Views ###############################
'''

@isAuthenticated
def addStudentToModule(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    lists = request.POST.lists()
    students =lists[2]
    module = lists[3]
    print "Super details::::: lalaalalalalalalalalalal"
    print students[1]
    print module[1][0]
    data ={
        'student':students[1],
        'module':module[1][0]
    }
    result = views.addStudentToModule(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] ==  1:
        Person = res[0]['Users']
        Modules = res[0]['Modules']
        return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':Person,
                                                                       'Modules':Modules,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))
    else:
        Person = res[0]['Users']
        Modules = res[0]['Modules']
        return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':Person,
                                                                       'Modules':Modules,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))

@isAuthenticated
def addLectureToModule(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    lists = request.POST.lists()
    lecture =lists[0]
    module = lists[2]
    print "Super details::::: lalaalalalalalalalalalal"
    print lists
    print lecture[1]
    print module[1][0]
    data ={
        'lecture':lecture[1],
        'module':module[1][0]
    }
    result = views.addLectureToModule(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] ==  1:
        Person = res[0]['Users']
        Modules = res[0]['Modules']
        return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':Person,
                                                                       'Modules':Modules,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))
    else:
        Person = res[0]['Users']
        Modules = res[0]['Modules']
        return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':Person,
                                                                       'Modules':Modules,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))
@isAuthenticated
def addTutorToModule(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    lists = request.POST.lists()
    tutor =lists[3]
    module = lists[2]
    print "Super details::::: lalaalalalalalalalalalal"
    print tutor[1]
    print module[1][0]
    data ={
        'tutor':tutor[1],
        'module':module[1][0]
    }
    result = views.addTtToModule(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] ==  1:
        Person = res[0]['Users']
        Modules = res[0]['Modules']
        return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':Person,
                                                                       'Modules':Modules,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))
    else:
        Person = res[0]['Users']
        Modules = res[0]['Modules']
        return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':Person,
                                                                       'Modules':Modules,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))

@isAuthenticated
def removeStudentFromModule(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    lists = request.POST.lists()
    students =lists[2]
    module = lists[3]
    print "Super details::::: lalaalalalalalalalalalal"
    print students[1]
    print module[1][0]
    data ={
        'student':students[1],
        'module':module[1][0]
    }
    result = views.removeStudentFromModule(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] ==  1:
        Person = res[0]['Users']
        Modules = res[0]['Modules']
        return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':Person,
                                                                       'Modules':Modules,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))
    else:
        Person = res[0]['Users']
        Modules = res[0]['Modules']
        return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':Person,
                                                                       'Modules':Modules,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))

@isAuthenticated
def removeLectureFromModule(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    lists = request.POST.lists()
    lecture =lists[0]
    module = lists[3]
    print "Super details::::: lalaalalalalalalalalalal"
    print lecture[1]
    print module[1][0]
    data ={
        'lecture':lecture[1],
        'module':module[1][0]
    }
    result = views.removeLectureFromModule(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] ==  1:
        Person = res[0]['Users']
        Modules = res[0]['Modules']
        return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':Person,
                                                                       'Modules':Modules,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))
    else:
        Person = res[0]['Users']
        Modules = res[0]['Modules']
        return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':Person,
                                                                       'Modules':Modules,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))

@isAuthenticated
def removeTutorFromModule(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    lists = request.POST.lists()
    tutor =lists[0]
    module = lists[2]
    print "Super details::::: lalaalalalalalalalalalal"
    print tutor[1]
    print module[1][0]
    data ={
        'tutor':tutor[1],
        'module':module[1][0]
    }
    result = views.removeTutorFromModule(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] ==  1:
        Person = res[0]['Users']
        Modules = res[0]['Modules']
        return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':Person,
                                                                       'Modules':Modules,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))
    else:
        Person = res[0]['Users']
        Modules = res[0]['Modules']
        return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':Person,
                                                                       'Modules':Modules,
                                                                       'user_roles':user_roles},context_instance = RequestContext(request))

def addModule(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    code = request.POST['code']
    name = request.POST['name']
    
    data = {
        'code':code,
        'name':name
    }
    results = views.addModule(request,json.dumps(data))
    res = json.loads(results.content)
    
    reslt = views.getUserInDataBase(request)
    rslt = json.loads(reslt.content)
    if res[0]['type'] == 1:
        if rslt[0]['type'] == 1:
            person = rslt[0]['User']
            module = rslt[0]['Modules']
            return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':person,
                                                                       'Modules':module,
                                                                       'user_roles':user_roles,'moduleAdded':1},context_instance = RequestContext(request))
    else:
        if rslt[0]['type'] == 1:
            person = rslt[0]['User']
            module = rslt[0]['Module']
            return render_to_response("web_interface/admin.htm",{'default_user':default_user,
                                                                       'user_lect':user_lect,
                                                                       'user_stud':user_stud,
                                                                       'user_tut':user_tut,
                                                                       'user_ta':user_ta,
                                                                       'Person':person,
                                                                       'Modules':module,
                                                                       'user_roles':user_roles,'moduleAdded':1},context_instance = RequestContext(request))

def import_csv(request):
    user_type = ''
    default_user =''
    user_roles = []
    user_lect = []
    user_stud = []
    user_tut = []
    user_ta = []
    user = request.session['user']
    
    if len(user['lecturerOf']) != 0:
            user_type = 'LC'
            user_lect.append({user_type:user['lecturerOf']})
            user_roles.append('Lecturer')
                        
    if len(user['studentOf']) != 0:
            user_type ='ST'
            user_stud.append({user_type:user['studentOf']})
            user_roles.append('Student')
                        
    if len(user['tutorFor']) != 0:
            user_type = 'TT'
            user_tut.append({user_type:user['tutorFor']})
            user_roles.append('Tutor')
                        
    if len(user['teachingAssistantOf']) != 0:
            user_type ='TA'
            user_ta.append({user_type:user['teachingAssistantOf']})
            user_roles.append('Teaching ass')
                        
    #choosing the default user based on the user type ie,lecturer
    if len(user['lecturerOf']) != 0:
        default_user = 'LC'
    elif len(user['studentOf']) != 0:
        default_user = 'ST'
    elif len(user['tutorFor']) != 0:
        default_user = 'TT'
    else:
        default_user = 'TA'
    
    assess_id = request.POST['assess_id']
    module = request.POST['module']
    result = repo.import_csv(request)
    
    res = json.loads(result.content)
    
    if res['type'] == 1:
        data={
            'assess_id':assess_id
        }
    
        result = views.assessmentCenterLeaf(request,json.dumps(data))
        res = json.loads(result.content)
        if res['type'] ==1:
            assessmentName = res['assessmentName']
            average = res['average']
            median = res['median']
            mode = res['mode']
            frequency = res['frequency']
            stddev = res['stddev']
            studentlist = res['students']
            pass_fail_percentage = res['pass_fail_percentage']
    
            return render_to_response("web_interface/leaf_assessment_center.htm",{'default_user':default_user,
                                                                            'user_lect':user_lect,
                                                                            'user_stud':user_stud,
                                                                            'user_tut':user_tut,
                                                                            'user_ta':user_ta,
                                                                            'user_roles':user_roles,
                                                                            'average':average,'median':median,'mode':mode,'frequency':frequency,
                                                                            'stddev':stddev,'studentlist':studentlist,
                                                                            'assess_id':assess_id,'assessmentName':assessmentName,
                                                                            'module':module, 'pass_fail_percentage':pass_fail_percentage}, context_instance=RequestContext(request))
    
        else:
            return render_to_response("web_interface/leaf_assessment_center.htm",{'default_user':default_user,
                                                                    'user_lect':user_lect,
                                                                    'user_stud':user_stud,
                                                                    'user_tut':user_tut,
                                                                    'user_ta':user_ta,
                                                                    'user_roles':user_roles,'agg_name':agg_name, 'numChildren':numChildren,'message':message,
                                                                    'children':children, 'assess_id':assess_id,'assessmentName':assessmentName, 'module':module}, context_instance=RequestContext(request))