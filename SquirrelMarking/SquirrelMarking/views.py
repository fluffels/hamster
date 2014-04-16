from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from businessLogicAPI import *
from forms import *
from django.shortcuts import render
#from django.http import HttpResponseRedirect

@csrf_protect
def loginWeb(request):
	nform = LoginForm() 
	if request.method == 'POST': # If the form has been submitted...		
		# ContactForm was defined in the the previous section
		form = LoginForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
		# Process the data in form.cleaned_data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			try:
				login(request,username,password)
				try:
					P = getSessionPerson(request)
					SOCourses = P.studentOf
					TOCourses = P.tutorOf
					TAOCourses = P.teachingAssistantOf
					LOCourses = P.lectureOf
					
					#~ SOlist = []
					#~ for mod in SOCourses:
						#~ y = getAllSessionsForModule(mod)
						#~ SOlist.append(y)
						
					#~ TOlist = []
					#~ for mod in TOCourses:
						#~ y = getAllSessionsForModule(mod)
						#~ TOlist.append(y)

					#~ TAOlist = []
					#~ for mod in TAOCourses:
						#~ y = getAllSessionsForModule(mod)
						#~ TAOlist.append(y)

					#~ LOlist = []
					#~ for mod in LOCourses:
						#~ y = getAllSessionsForModule(mod)
						#~ LOlist.append(y)	
					
					print (P.firstName)
					return render(request,'index.html', {'person': P})#, 'studentOf':SOlist, 'tutorOf':TOlist, 'teachingAssistantOf':TAOlist, 'lectureOf':LOlist}) # Redirect after POST
				except Exception, e:
					print (e)
					return render(request,'login.html', {'form': nform, 'msg':"Session ERROR"})					
			except Exception:
				return render(request,'login.html', {'form': nform, 'msg':"Invalid details entered"})
		else:
			return render(request,'login.html', {'form': nform, 'msg':form.errors})#form.errors
	else:	
		return render(request,'login.html', {'form': nform})
		
		
def viewAssessments(request, mod_code):
	try:
		P = getSessionPerson(request)
		Assessments = getAllAssessmentsForModule(mod_code)
		return render(request,'div.html', {'Assessments': Assessments})		
	except:
		return render(request,'login.html', {'form': nform,  'msg':"Please login"})
		
'''
    REPORTING FUNCTIONS
'''
# frequency analysis function to initialize variables	
def frequency_analysis(request):
        person = Person()
        return render_to_response('studentChosen.html',{'per': person,} )

def getLeafAssessments(request):
        person = getSessionPerson(request)
        assess_id = request.POST['assess_id']
        x = getLeafAssessmentMarksOfAsssessmentForStudent(person.upId, assess_id)
        return render_to_response( 'studentChosen.html', {'leafAssessmentList' : x})
        
def  getAssessments(request):
        person = getPresonByID(request.POST['studentID'])
        leaf = request.POST['leafAssessment']
        leafAssesment = getLeafAssesment() #function does not exist, make it!!!!!
        type = request.POST['type']
        assessmentList = getAllAssessmentTotalsForStudent(person.empl_no, request.POST['mod_code'])
        return render_to_response( 'studentChosen.html', {'per' : person, 'usrAllAssessments' : assessmentList, 'type' : type, 'leafAssesment' : leafAssesment })

def audit_report(request):
	t = get_template('auditReport.html')
	html = t.render(Context())
	return HttpResponse(html)
	
def reporting_main(request):
	t = get_template('Reporting_Main.html')
	html = t.render(Context())
	return HttpResponse(html)
        
def studentModules(request):
        student = getSessionPerson(request)
        render_to_response('studentChosen.html', {'modules' : student.getAllModulesForStudent()})        
        
def getLecturerModules(request):
        lecturer = getSessionPerson(request)
        return render_to_response('assessmentReport.html', {'modules' : getAllModulesForLecturer(lecturer.upId)})
        
def searchStudents(request):
        searchedItemRequest = request.POST['searchedItem']
        students = findPerson(searchedItemRequest) #function does not exist, make it!!!!!
        render_to_response('studentChosen.html', {'students' : students})
        
def displayStudent(request):
	person = getStudentByID(request.POST['upId'])
	render_to_response('studentReport.html', {'person' : person})
'''
    END REPORTING FUNCTIONS
'''