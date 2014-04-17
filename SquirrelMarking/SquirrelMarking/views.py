from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from dbModels.models import *
from ldapView import *
from businessLogicAPI import *
from forms import *
from django.shortcuts import render
from reportRenderers import *

#from django.http import HttpResponseRedirect

def ldapTest(request):
	try:
		return HttpResponse("<table border='1' style='width:1000px'>"+ 
			"<tr>"+
			"<td>Authenticate User Object</td>" +
			"<td>"+ str(authenticateUser(request,"u89000447","Herbert"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Enrollments of user</td>" +
			"<td>"+str(sourceEnrollments("u89000447"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td> Tuter Designations</td>" +
			"<td>"+str(sourceTutorDesignations("u89000447"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>TeachAsst Designations</td>" +
			"<td>"+str(sourceTeachingAssistantDesignations("u89000915"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Lecturer Designations</td>" +
			"<td>"+str(sourceLecturerDesignations("BWingfield"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Demographics of User </td>" +
			"<td>"+str(sourceDemographics("BWingfield"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Members of Module </td>" +
			"<td>"+str(getMembers("stud_COS301"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Find a user by attribute</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Tries to look up a student</td>" +
			"<td>"+str(findPerson("uid","u89000447"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Prints all module codes </td>" +
			"<td>"+str(getAllModuleCodes())+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td> Prints Students of a module </td>" +
			"<td>"+str(getStudentsOf("COS300"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Prints Tutors of a module</td>" +
			"<td>"+str(getTutorsOf("COS344"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Prints TAs of a module</td>" +
			"<td>"+str(getTAsOf("COS110"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Prints Lecturers of a module</td>" +
			"<td>"+str(getLecturorsOf("COS301"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Test * character</td>" +
			"<td>"+ str(authenticateUser(request,"u89000447","Herbert"))+"</td>" +
			"</tr> "+
			"<tr>"+
			"<td> " +"</td>" +
			"</tr>"+
			"<tr>"+
			"<td> " +"</td>" +
			"</tr>"+
			"<tr>"+
			"<td>Authenticate User Object</td>" +
			"<td>"+ str(authenticateUser(request,"u89000447","Herbert"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Enrollments of user test char * </td>" +
			"<td>"+str(sourceEnrollments("u8*"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td> Tuter Designations test char + </td>" +
			"<td>"+str(sourceTutorDesignations("u8900044+"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>TeachAsst Designations test char $ </td>" +
			"<td>"+str(sourceTeachingAssistantDesignations("u8900091$"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Lecturer Designations test char # </td>" +
			"<td>"+str(sourceLecturerDesignations("##########"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Demographics of User test char \ n </td>" +
			"<td>"+str(sourceDemographics("BWingfie\n"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Members of Module </td>" +
			"<td>"+str(getMembers("stud_COS301"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Find a user by attribute</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Tries to look up a student test char @</td>" +
			"<td>"+str(findPerson("uid","u8900044@"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td> Prints Students of a module </td>" +
			"<td>"+str(getStudentsOf("*"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Prints Tutors of a module</td>" +
			"<td>"+str(getTutorsOf("COS344"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Prints TAs of a module test char _ </td>" +
			"<td>"+str(getTAsOf("COS11_"))+"</td>" +
			"</tr> "+ 
			"<tr>"+
			"<td>Prints Lecturers of a module test char - </td>" +
			"<td>" + str(getLecturorsOf("COS30-")) +"</td>" +
			"</tr> " +  
			"</table>");
	except Exception,e:
		raise e
		
def importTest(request):
	fo.close()
	t = get_template('login.html')
	html = t.render(Context())
	return HttpResponse(html)
	
def reportTest(request):
	dataOut = renderAssessmentReport("COS301", 1)
	return HttpResponse(dataOut)

def test(request):
	
	string = "<h1>Business Logic</h1>"
	string += "<p><h2>populateModules</h2>"
	populateModules()
	
	string += "</p><p><h2>getAllModules</h2>"
	for module  in getAllModules():
		string += "<br/>" + module.code
	sting += "</p>"
	return HTTPResponse(string)
	print "getPersonListFromArrayList"
	studentNumber = []
	studentNumber.append("u89000960")
	studentNumber.append("u89000961")
	studentNumber.append("u89000962")
	for person  in getPersonListFromArrayList(studentNumber):
		print person.getupId()
	
	print "getAllLecturesOfModule"		
	
	for lecmodel  in getAllLecturesOfModule(getAllModules()[0].code):
		print lecmodel.getupId()
		
	print "getAllStudentsOfModule"
	for lecmodel  in getAllStudentsOfModule(getAllModules()[0].code):
		print lecmodel.getupId()	

	print "getAllTAsOfModule"
	for lecmodel  in getAllTAsOfModule(getAllModules()[0].code):
		print lecmodel.getupId()	
		
	print "getAllNamesOf in this case TA"
	person = getAllTAsOfModule(getAllModules()[0].code)
	for lecmodel  in getAllNamesOf(person):
		print lecmodel
	
	print "getAllTutorsOfModule"
	for lecmodel  in getAllTutorsOfModule(getAllModules()[0].code):
		print lecmodel.getupId()	
		
	print "getAllMarkersOfModule"
	for lecmodel  in getAllMarkersOfModule(getAllModules()[0].code):
		print lecmodel.getupId()	
	
	print "getAssessment"
	for temp in getAssessment():
		print temp.getName()
			
	print "getAssessmentForModuleByName"
	for temp in getAssessmentForModuleByName(getAllModules()[1].code, getAssessment()[0].getName()):
		print temp
	
	print "getLeafAssessmentOfAssessmentForModuleByName"
	for temp in getLeafAssessmentOfAssessmentForModuleByName(getAllModules()[1].code, getAssessment()[0].getName(), 'test'):
		print temp
		
	print "getAllAssessmentsForModule"
	for temp in getAllAssessmentsForModule(getAllModules()[1].code):
		print temp
	
	print "getAllOpenAssessmentsForModule"
	for temp in getAllOpenAssessmentsForModule(getAllModules()[1].code):
		print temp
		
	print "getAllOpenAssessmentsForModule"
	for temp in getAllOpenAssessmentsForModule(getAllModules()[1].code):
		print temp
	
	print "getAllModulesForStudent"
	for temp in getAllModulesForStudent('u89000847'):
		print temp
		
	print "getAllModulesForMarker"
	for temp in getAllModulesForMarker('u89000999'):
		print temp
	
	print "getAllModulesForLecturer"
	for temp in getAllModulesForLecturer('ALeffley'):
		print temp
	
	print "getAllLeafAssessmentsForAssessment"
	#re-check functionality
	for temp in getAllLeafAssessmentsForAssessment(getAssessment()[1].getID()):
		print temp
	
	print "getAllAssementsForStudent"
	for temp in getAllAssementsForStudent('u89000847', 'COS301'):
		print temp.getName()
		
	print "getAllSessionsForModule"
	for temp in getAllSessionsForModule('COS301'):
		print temp
		
	print "getLeafAssessmentMarksOfAsssessmentForStudent"
	for temp in getLeafAssessmentMarksOfAsssessmentForStudent(studentNumber[0],getAssessment()[1].getID()):
		print temp
		
	print "getAllAssessmentTotalsForStudent"
	for temp in getAllAssessmentTotalsForStudent('u89000999',getAllModules()[1].code):
		print temp
	#createAssessment(request, "test",123,"asd",getAllModules()[1])
	#print "getAssessmentForModuleByName"
	#a=getAssessmentForModuleByName(getAllModules()[1],"test")
	#print a.getName()
	#print "createLeafAssessment"
	#createLeafAssessment(request,"Task1",a,20)
	
	
	#print "createAssessment"
	#done 

	#x2 = insertModule("COS301")
	#x3 = insertAssessment('test','asdas',"type",x2)
	#x4 = insertSessions("test",x3,'2012-12-12 12:12','2015-12-12 12:12')
	#xx = insertMarkSession("u89000999",x4)
	#x5 = insertMarkerModule("u89000999",x2)
	#x6 = insertLeafAssessment("name",x3,100,True)
	#x7 = insertMarkAllocation(x6,20,x4,"asdsad","sadasd",'2012-12-12 12:12')
	#x8 = insertMarkerModule("u89000999",x2)
	#login(request,"u89000989","Flanigan")
	#p = getSessionPerson(request)
	#print (p.studentOf)
	#print (p.firstName)
	#removeMarkerFromModule("COS301","asdasd")
	#removeSession(x4.getID())
	#print getAllSessionsForModule("COS301")
	#createAssessment(request, "test",123,"asd",x2)
	#closeSession(request,1)
	#removeSession(request,1)
	#removeMarkerFromSession(request,2,"u89000999")
	#createMarkAllocation(request, 1,1,"someperson","someotherperson",'2012-12-12 12:12')
	#updateMarkAllocation(request, 1,0)
	#removeMarkerFromModule(request,"COS301","u89000999")
	#setMarkerForModule(request,"u89000999",x2)
	#print getSessionByName("COS301","test")
	#print getMarkAllocationFromID(2)
	#getAuditLogFromTimeRange('2012-12-12 12:12','2015-12-12 12:12')
	#print getAllOpenAssessmentsForModule("COS301")
	#print getAuditLogFromTableName("MarkerSessions")
	return HttpResponse("<html><body><p>"+str(len(getOpenSessions(2)))+"</p><p>"+str(getSessions()[0].assessment_id_id)+"</p></body></html>")

#def logout(request)

def loginData(request):
	t = get_template('login.html')
	html = t.render(Context())
	return HttpResponse(html)

	
def student_home(request):
	t = get_template('student.html')
	html = t.render(Context())
	return HttpResponse(html)
	
def lecturer_home(request):
	t = get_template('lecturer.html')
	html = t.render(Context())
	return HttpResponse(html)
	
def marker_home(request):
	t = get_template('marker.html')
	html = t.render(Context())
	return HttpResponse(html)

def loginData(request):
	t = get_template('login.html')
	html = t.render(Context())
	return HttpResponse(html)

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
			except Exception, e:
				print (e)
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

def assessment_view(request):
	t = get_template('assessmentView.html')
	html = t.render(Context())
	return HttpResponse(html)

def assessment_manager(request):
	t = get_template('assessmentManager.html')
	html = t.render(Context())
	return HttpResponse(html)

def session_manager(request):
	t = get_template('sessionManager.html')
	html = t.render(Context())
	return HttpResponse(html)
	
	
	
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
def statistics(request):
	t = get_template('Statistics.html')
	html = t.render(Context())
	return HttpResponse(html)

def student_chosen(request):
	t = get_template('studentChosen.html')
	html = t.render(Context())
	return HttpResponse(html)

def student_report(request):
	t = get_template('studentReport.html')
	html = t.render(Context())
	return HttpResponse(html)
	
	
def unpublish(request):
	t = get_template('unpublish.html')
	html = t.render(Context())
	return HttpResponse(html)

def marks_management(request):
        t = get_template('marks-management.html')
	html = t.render(Context())
	return HttpResponse(html)	
	
def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    print >>sys.stderr, 'Goodbye, cruel world!'
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticateUser(username, password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('home.html')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Squirrel account is not active.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)
