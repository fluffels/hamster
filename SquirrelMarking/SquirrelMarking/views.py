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
from DBAdapter import *
from Reporting.CSVReportGenerator import *
from Reporting.PDFReportGenerator import *
from django.core.files.base import ContentFile
import datetime
from django.utils.timezone import utc

#from DBAdapter import *
import sys
import csv
import StringIO
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
	with open("SquirrelMarking/data.csv", "rb") as csvFile:
		parseMarksToDB(request, csvFile)
	return HttpResponse("<p>imported</p>")
	
def AssReportTest(request):
	dataOut = renderAssessmentReport("COS301", 1)
	return HttpResponse(dataOut)

def studReportTest(request):
	dataOut = renderStudentReport("COS301", "u89000583", 26)
	return HttpResponse(dataOut)

def auditReportTest(request):
	login(request,"u89000583","Mason")
	createAssessment(request,"test",50,"thingamabob",Module.objects.get(code="COS301"))
	dataOut = renderAuditReport("COS301", "u89000583", "" ,'2012-12-12 12:12','2015-04-20 12:12')
	return HttpResponse(dataOut)
	
def PDFAssReportTest(request):
	response     = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="AssessmentReport.pdf"'
	reportGenerator = PDFReportGenerator()
	testReport = reportGenerator.generateAssessmentReport("COS301", 1,response)
	return response 
	
def PDFstudReportTest(request):
	response     = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="StudentReport.pdf"'
	reportGenerator = PDFReportGenerator()
	testReport = reportGenerator.generateStudentMarksReport("COS301", "u89000583", 1,response)
	return response 
	
def PDFauditReportTest(request):
	login(request,"u89000583","Mason")
	createAssessment(request,"test",50,"thingamabob",Module.objects.get(code="COS301"))
	response     = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="AuditReport.pdf"'
	reportGenerator = PDFReportGenerator()
	testReport = reportGenerator.generateAuditReport("COS301", "u89000583", "" ,'2012-12-12 12:12','2015-04-20 12:12',response)
	return response 
	
def CSVAssReportTest(request):
	reportGenerator = CSVReportGenerator()
	testReport = reportGenerator.generateAuditReport("COS301", 1)
	response     = HttpResponse(testReport, content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="AssessmentReport.csv"'
	return response 
	
def CSVstudReportTest(request):
	reportGenerator = CSVReportGenerator()
	testReport = reportGenerator.generateStudentMarksReport("COS301", "u89000583", 1)
	file_to_send = ContentFile(testReport)
	response     = HttpResponse(testReport,'application/csv')
	response['Content-Disposition'] = 'attachment; filename="StudentReport.csv"'
	return response 
	
def CSVauditReportTest(request):
	login(request,"u89000583","Mason")
	createAssessment(request,"test",50,"thingamabob",Module.objects.get(code="COS301"))
	reportGenerator = CSVReportGenerator()
	testReport = reportGenerator.generateAuditReport("COS301", "u89000583", "" ,'2012-12-12 12:12','2015-04-20 12:12')
	response     = HttpResponse(testReport,'text/csv')
	response['Content-Disposition'] = 'attachment; filename="AuditReport.csv"'
	return response 

def PDFAssReportTest(request):
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="AssessmentReport.pdf"'
	reportGenerator = PDFReportGenerator()
	testReport = reportGenerator.generateAssessmentReport("COS301", 1,response)
	return response

def PDFstudReportTest(request):
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="StudentReport.pdf"'
	reportGenerator = PDFReportGenerator()
	testReport = reportGenerator.generateStudentMarksReport("COS301", "u89000583", 1,response)
	return response

def PDFauditReportTest(request):
	login(request,"u89000583","Mason")
	createAssessment(request,"test",50,"thingamabob",Module.objects.get(code="COS301"))
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="AuditReport.pdf"'
	reportGenerator = PDFReportGenerator()
	testReport = reportGenerator.generateAuditReport("COS301", "u89000583", "" ,'2012-12-12 12:12','2015-04-20 12:12',response)
	return response

def CSVAssReportTest(request):
	reportGenerator = CSVReportGenerator()
	testReport = reportGenerator.generateAuditReport("COS301", 1)
	response = HttpResponse(testReport, content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="AssessmentReport.csv"'
	return response

def CSVstudReportTest(request):
	reportGenerator = CSVReportGenerator()
	testReport = reportGenerator.generateStudentMarksReport("COS301", "u89000583", 1)
	file_to_send = ContentFile(testReport)
	response = HttpResponse(testReport,'application/csv')
	response['Content-Disposition'] = 'attachment; filename="StudentReport.csv"'
	return response

def CSVauditReportTest(request):
	login(request,"u89000583","Mason")
	createAssessment(request,"test",50,"thingamabob",Module.objects.get(code="COS301"))
	reportGenerator = CSVReportGenerator()
	testReport = reportGenerator.generateAuditReport("COS301", "u89000583", "" ,'2012-12-12 12:12','2015-04-20 12:12')
	response = HttpResponse(testReport,'text/csv')
	response['Content-Disposition'] = 'attachment; filename="AuditReport.csv"'
	return response 

def test(request):
	
	print "populateModules"
	populateModules()
	
	print "getAllModules"
	for module  in getAllModules():
		print module.code
	
	print "getPersonListFromArrayList"
	studentNumber = []
	studentNumber.append("u89000960")
	studentNumber.append("u89000961")
	studentNumber.append("u89000962")
	for person  in getPersonListFromArrayList(studentNumber):
		print person.upId

	print "getAllLecturesOfModule"		

	for lecmodel  in getAllLecturesOfModule(getAllModules()[0].code):
		print lecmodel.upId

	print "getAllStudentsOfModule"
	for lecmodel  in getAllStudentsOfModule(getAllModules()[0].code):
		print lecmodel.upId	

	print "getAllTAsOfModule"
	for lecmodel  in getAllTAsOfModule(getAllModules()[0].code):
		print lecmodel.upId	

	print "getAllNamesOf in this case TA"
	person = getAllTAsOfModule(getAllModules()[0].code)
	for lecmodel  in getAllNamesOf(person):
		print lecmodel

	print "getAllTutorsOfModule"
	for lecmodel  in getAllTutorsOfModule(getAllModules()[0].code):
		print lecmodel.upId	

	print "getAllMarkersOfModule"
	for lecmodel  in getAllMarkersOfModule(getAllModules()[0].code):
		print lecmodel

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

def logoutWeb(request):
    try:
	logout(request);
    except Exception, e:
	print (e)
    return render(request,'logout.html', {})
    
@csrf_protect
def loginWeb(request):
    try:
	P = getSessionPerson(request)
	return render(request,'index.html', {'person': P})
    except:
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
					#class Person1:
					    #firstName = "FirstNameHere"
					    #upId = "123456789"
					    #surname = "SurnameHere"
					    #studentOf  = ['COS123','COS321'] #module
					    #tutorOf  = ['COS456','COS654'] #module
					    #teachingAssistantOf  = ['COS789','COS987'] #module
					    #lectureOf = ['COS135','COS790']
					#P = Person1()					
					#print (P.firstName)
					return render(request,'index.html', {'person': P})
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

		
def getCourseAssessments(request):
	junk = 'remove this junk comments'
	#class Person1:
	    #firstName = "FirstNameHere"
	    #upId = "123456789"
	    #surname = "SurnameHere"
	    #studentOf  = ['COS123','COS321'] #module
	    #tutorOf  = ['COS456','COS654'] #module
	    #teachingAssistantOf  = ['COS789','COS987'] #module
	    #lectureOf = ['COS135','COS790']
	#P = Person1()
	
	
	#class Assessment1():
	  #assessment_name="ass1"
	  #assessment_weight="59"
	  #assessment_type="Prac"
	  #module_id =request.POST['mod_code']
	  #id='1'
	  
	#class Assessment2():
	  #assessment_name="ass2"
	  #assessment_weight="76"
	  #assessment_type="Prac"
	  #module_id =request.POST['mod_code']
	  #id='1'
	  
	#class Assessment3():
	  #assessment_name="ass3"
	  #assessment_weight="23"
	  #assessment_type="Prac"
	  #module_id =request.POST['mod_code']
	  #id='1'
	  
	#Assessments=[]
	#print (Assessment1())
	#Assessments.append(Assessment1())
	#Assessments.append(Assessment2())
	#Assessments.append(Assessment3())	
	
	P = getSessionPerson(request)	
	c = request.POST['mod_code']
	ObjectList = []
	role = ""
	try:
	  if c in P.studentOf:
	    role='student'
	    Assessments = getAllAssementsForStudent(P.upId, c)# getAllAssessmentsForModule(c)#
	    for assessment in Assessments:
	      list = []
	      assessmentTotal = getAssessmentTotalForStudent(P.upId,c,assessment.id)
	      list.append(assessment)
	      list.append(assessmentTotal)
	      ObjectList.append(list)	
	  else:  
	    Assessments = getAllOpenAssessmentsForModule(c)
	    if c in P.tutorOf:
	      role='tutor'
	      for assessment in Assessments:
		list = []
		sessions = getOpenSessionsForMarker(assessment.id, P.upId)
		list.append(assessment)
		list.append(sessions)
		ObjectList.append(list)	  
	    else:  
	      if c in P.teachingAssistantOf:
		role='teachingAssistant'
		for assessment in Assessments:
		  list = []
		  sessions = getOpenSessionsForMarker(assessment.id, P.upId)
		  list.append(assessment)
		  list.append(sessions)
		  ObjectList.append(list)
	      else:   
		if c in P.lectureOf:
		  role='lecturer'
		  Assessments = getAllAssessmentsForModule(c)
		  for assessment in Assessments:
		    list = []
		    sessions = getOpenSessions(assessment.id)
		    list.append(assessment)
		    list.append(sessions)
		    ObjectList.append(list) 
	except Exception, e:
	  print (e)
	return render(request,'listAssessments.html', {'ObjectList': ObjectList, 'C': c, 'role': role})
	
def viewAssessmentsOptions(request, Marker=None):
	c = request.POST['mod_code']
	Assessments = ''
	if Marker:
		Assessments = getAllAssementsForStudent(Marker)
	else:
		Assessments = getAllAssessmentsForModule(c)
	return render(request,'listAssessmentsOptions.html', {'Assessments': Assessments})	

def viewAssessmentSessionsOptions(request):
	c = request.POST['mod_code']
	a = request.POST['assess_id']
	P = getSessionPerson(request)
	Sessions = getOpenSessions(a)
	return render(request,'listAssessmentSessionsOptions.html', {'Sessions': Sessions})

class Student:
	firstName = ""
	upId = ""
	surname = ""
	total = ""
	def __init__(self):
		self.firstName = ''
		self.upId = ''
		self.surname = ''
		self.total  = 0
	def setfirstName(self,value):
		  self.firstName=value
	def setupId(self,value):
		  self.upId=value
	def setsurname(self,value):
		  self.surname=value
	def setTotal(self,value):
		  self.total=value
	def __unicode__(self):
		return self.firstName+" "+self.surname+" "+self.upId	
	
	
def getAssessmentStudentMarks(request):
	m = request.POST['mod_code']
	a = request.POST['assess_id']
	students = getAllStudentsOfModule(m)	
	weight = getAssessmentFromID(a).assessment_weight
	list = []	
	for student in students:
		stud = Student()
		stud.setfirstName(student.getfirstName())
		stud.setupId(student.getupId)
		stud.setsurname(student.surname)
		stud.setTotal(getAssessmentTotalForStudent(student.upId, m, a))
		list.append(stud)  
	return render(request,'AssessmentStudentMarksTable.html', {'StudentMarks': list, 'weight' : weight})
  
def getSessionStudentMarks(request):
	m = request.POST['mod_code']
	a = request.POST['assess_id']
	s = request.POST['sess_id']
	session = getSessionsFromID(s)
	students = getStudentsForASession(s)
	weight = session.assessment_id.assessment_weight
	
	list = []	
	for student in getPersonListFromArrayList(students):
		stud = Student()
		stud.setfirstName(student.getfirstName())
		stud.setupId(student.getupId)
		stud.setsurname(student.surname)
		stud.setTotal(getAssessmentTotalForStudent(student.upId, m, a))
		list.append(stud)  
	return render(request,'AssessmentStudentMarksTable.html', {'StudentMarks': list, 'weight' : weight})

def getLeafAssessmentStudentMarks(request):
	
	m = request.POST['mod_code']
	a = request.POST['assess_id']
	studentID = request.POST['student_uid']
	leafAssessmentList = getLeafAssessmentMarksOfAsssessmentForStudent(studentID, getAssessmentFromID(a))
	return render(request,'LeafAssessmentStudentMarksTable.html', {'leafAssessments': leafAssessmentList})  

def setmark_allocation(request):
	P = getSessionPerson(request)
	name = request.POST['name']
	mark = request.POST['mark']
	leaf_id = request.POST['leaf_id']
	session_id = request.POST['session_id']
	student = request.POST['student_uid']
	
	leaf = createMarkAllocation(request, leaf_id, session_id, marker, student, timestamp)
	updateMarkAllocation(request, leaf, mark)
	return response(request, 'marks-management.html')
	
def assessment_view(request):
    m = "COS110"#request.POST['mod_code']
    class Person1:
	firstName = "FirstNameHere"
	upId = "123456789"
	surname = "SurnameHere"
	studentOf  = ['COS110','COS321'] #module
	tutorOf  = ['COS456','COS654'] #module
	teachingAssistantOf  = ['COS789','COS987'] #module
	lectureOf = ['COS135','COS790']
	
    class Assessment1():
	  assessment_name="ass1"
	  assessment_weight="59"
	  assessment_type="Prac"
	  module_id ="COS110"
    
    listMark = []
    list = []
    list.append("ass1")
    list.append("10")
    list.append("8")
    listMark.append(list)
	
    P = Person1()
 
def checkUserRole(role, course, assessment):
    P = getSessionPerson(request) 
    if role == 'student':
      if course in P.studentOf:
	return 1
    if role == 'tutor':  
      if course in P.tutorOf:
	return 1
    if role == 'teachingAssistant':  
      if course in P.teachingAssistantOf:
	return 1
    if role == 'lecture':  
      if course in P.lectureOf:
	return 1


'''Student Assessment'''
def studentPage(request, course, assessment=None):
    P = getSessionPerson(request) 
    Assessments = getAllAssementsForStudent(P.upId, course) #getAllAssessmentsForModule(course)#
    if (assessment):
      SpecificA = getAssessmentFromID(assessment)
      return render(request,'studentAssessment.html', {'C': course, 'A': assessment,'StudentAssessments': Assessments, 'Specific': SpecificA})
    return render(request,'studentAssessment.html', {'C': course, 'A': assessment,'StudentAssessments': Assessments})
    
def getLeafAssessmentsTableWeb(request): 
    P = getSessionPerson(request) 
    a = request.POST['assess_id']
    assess = getAssessmentFromID(a);
    leafAssessmentList = getLeafAssessmentMarksOfAsssessmentForStudent(P.upId, assess)  
    return render(request,'tableLeafAssessmentMarks.html', {'leafAssessments': leafAssessmentList})  
    
'''Tutor Assessment'''      
def tutorPage(request, course, assessment=None, session=None):
	P = getSessionPerson(request) 
	request.POST['mod_code'] = course
	assessments = ''
	if assessment:		
		request.POST['assess_id'] = assessment		  
		if session:
			return render(request,'marks-management.html', {'Assessments': assessmentName, })
		else:
			viewAssessmentSessionsOptions(request, P.upId)  
	else:
		assessments = viewAssessmentsOptions(request, P.upId)
		return render(request,'marks-management.html', {'Assessments': assessmentName})
    
'''teachingAssistant Assessment'''  
def teachingAssistantPage(request, course, assessment=None, session=None):
	request.POST['mod_code'] = course
	request.POST['assess_id'] = assessment
	viewAssessmentsOptions(request)
	viewAssessmentSessionsOptions(request)
	if assessment:
		leafAssessment = getLeafAssessmentMarksOfAsssessmentForStudent(P.upId, assessment)    
		if session:
			leafAssessment = getLeafAssessmentMarksOfAsssessmentForStudent(P.upId, assessment) 
	return render(request,'marks-management.html', {'Assessments': assessmentName})  

    
'''Lecturer'''      
def manageCourse(request, course=None):
	P = getSessionPerson(request)
	Courses = P.lectureOf	
	msg = ''
	if course:
		if course in Courses:
			Tutors = getAllTutorsOfModule(course)
			TAs = getAllTAsOfModule(course)
			form = AssessmentManagerForm()
			if request.method == 'POST':
				form = AssessmentManagerForm(request.POST)
				if form.is_valid():
					AName = cleaned_data['Assessment_Name']
					AType = form.cleaned_data['Assessment_Type']
					AWeight = form.cleaned_data['Mark_Weight']
					if (request.POST['func'] == 'Add'):
						Module = getModuleFromID(course)
						createAssessment(request, AName,AWeight,AType,Module)
						msg = 'New Assessment Added'
					if (request.POST['func'] == 'Update'):
						assessmentID = request.POST['assessmentID']
						A = getAssessmentFromID(assessmentID)
						A.setName(AName)
						A.setType(AType)
						A.setWeight(AWeight)
						msg = "Assignment details updated" 
					if (request.POST['func'] == 'Remove'):
						assessmentID = request.POST['assessmentID']
						removeAssessment(request,assessmentID)
						msg = "Assignment has been removed" 
				else:
					msg = form.errors
			Assessments = getAllAssessmentsForModule(course)
			return render(request,'courseManager.html', {'C': course, 'Assessments':Assessments, 'Tutors': Tutors, 'TAs': TAs, 'form': form, 'msg': msg})
		else:
			return render(request,'error.html', {})
	else:
		return render(request,'courseManager.html', {'C': '', 'Courses':Courses})	    
		
def manageCourseAssessment(request, course, assessmentID):
	msg = ''
	A = getAssessmentFromID(assessmentID)
	if request.method == 'POST':		
		assessmentID = request.POST['assessmentID']
		A = getAssessmentFromID(assessmentID)
		if 'func' in request.POST:
			if (request.POST['func'] == 'Update Assessment'):
				form = AssessmentManagerForm(request.POST)
				if form.is_valid():
					AName = cleaned_data['Assessment_Name']
					AType = form.cleaned_data['Assessment_Type']
					AWeight = form.cleaned_data['Mark_Weight']				
					A.setName(AName)
					A.setType(AType)
					A.setWeight(AWeight)				
					msg = "Assignment details updated"    
		
		if 'funcLA' in request.POST:
			form = LeafAssessmentForm(request.POST)
			if form.is_valid():				
				if request.POST['funcLA'] == 'Update':
					leafA = getLeafAssessmentFromID(request.POST['leafID'])
					name = form.cleaned_data['name']
					maxMark = form.cleaned_data['maxMark']
					lname = leafA.leaf_name
					leafA.setName(name)
					leafA.setMax_mark(maxMark)
					msg = "LeafAssessment ("+lname+") updated ("+name+")"
					
				if request.POST['funcLA'] == 'Add':
					try:
						name = form.cleaned_data['name']
						maxMark = form.cleaned_data['maxMark']
						createLeafAssessment(request, name, A, maxMark)
						msg = "LeafAssessment ("+name+") added"
					except Exception, e:
						msg = "LeafAssessment could not be addded!"+str(e) 
					
				if request.POST['funcLA'] == 'Remove':	
					try:
						lname = form.cleaned_data['name']
						leafA = getLeafAssessmentOfAssessmentForModuleByName(course, A.assessment_name, lname)
						if leafA:
							removeLeafAssessment(request, leafA[0])
							msg = "LeafAssessment ("+lname+") removed" 
						else:
							msg = "LeafAssessment NOT removed!"
					except Exception, e:
						msg = "LeafAssessment NOT removed!"+str(e)  
			else:
				msg = form.errors 

		if 'funcS' in request.POST:
			form = SessionDetailsForm(request.POST)
			if form.is_valid():
				sessionLA = getSessionsFromID(request.POST['sessionID'])
				if request.POST['funcS'] == 'Update':
					print('hi')
				if request.POST['funcS'] == 'Add':
					session_name = form.cleaned_data['session_name']
					opentime = form.cleaned_data['open_date']
					closetime = form.cleaned_data['close_date']
					createSession(session_name,assessmentID, opentime, closetime)
					msg = "Session added"
					
				if request.POST['funcS'] == 'Remove':
					sname = sessionLA.session_name
					removeSession(request, sessionLA.id)
					msg = "Session ("+sname+") removed" 
			else:
				msg = form.errors 
	
	assessmentForm = AssessmentManagerForm()
	sessionForm = SessionDetailsForm()
	leafAssessmentForm = LeafAssessmentForm()
	#assessmentForm.cleaned_data['Assessment_Name'] = 'cos'
	#assessmentForm.cleaned_data['Assessment_Type'] = 'type'
	#assessmentForm.cleaned_data['Mark_Weight'] = 'weight'
	ASessions = getAllSessionsForAssessment(assessmentID)
	ALeafAssessments = getAllLeafAssessmentsForAssessment(A)
	return render(request,'assessmentManager.html', {'C': course, 'Assessment':A, 'LeafAssessments':ALeafAssessments, 'Sessions':ASessions, 'assessmentForm': assessmentForm, 'leafAssessmentForm': leafAssessmentForm, 'sessionForm': sessionForm, 'msg': msg})
	
def updateAssessmentInformation(request):  
  print ('hi')
  
def create_session(request):
	
	session = insertSession( request.POST['session_name'],request.POST['assessment_id'],request.POST['opened'],request.POST['closed'])
	studentList = request.POST['students']
	markerList = request.POST['markers']
	for student in studentList:
		insertStudentSessions(session.getSess_id, student)
	for marker in markerList:
		insertMarkerSessions(session.getSess_id, marker)
	return render_to_response( manage_session(request))
	
def manage_session(request):
	studentsList = getAllStudentsOfModule(request.POST['mod_code'])
	markersList = getAllMarkersOfModule(request.POST['mod_code'])
	return render(request, 'sessionManager.html', {'students' : studentsList, 'markers' : markersList })
	
def delete_session(request):
	sess_id = request.POST['session_id']
	removeSession(request, sess_id)
  
'''Lecturer Assessment'''  
def lecturerPage(request, course, assessment=None, session=None):
	P = getSessionPerson(request)
	modules = P.lectureOf
	Assessments = getAllAssessmentsForModule(course)	
	if session:    
		return render(request,'marks-management.html', {'modules': modules, 'C': course, 'A': assessment, 'S': session})
	if assessment: 
		return render(request,'marks-management.html', {'modules': modules, 'C': course, 'A': assessment})      
      
def openAssessment(request, assessmentName):
	print (assessmentName)
	return render(request,'assessmentView.html', {'Assessments': assessmentName})	

def marks_management(request):
	P = getSessionPerson(request)
	modules = P.lectureOf
	return render(request,'marks-management.html', {'modules': modules})
'''FORMS'''
    
class SaveAsPDFAssessment(forms.Form):
	AssID = forms.CharField(required=False)
	Module = forms.DateField(required=False)
	def __init__(self,*args,**kwargs):
		self.mod = kwargs.pop('mod')
		self.ass = kwargs.pop('ass')
		super(SaveAsPDFAssessment,self).__init__(*args,**kwargs)
		self.fields['Module'].widget = forms.HiddenInput(attrs={'value' : self.mod})
		self.fields['AssID'].widget = forms.HiddenInput(attrs={'value' : self.ass})

class SaveAsCSVAssessment(forms.Form):
	AssID = forms.CharField(required=False)
	Module = forms.DateField(required=False)
	def __init__(self,*args,**kwargs):
		self.mod = kwargs.pop('mod')
		self.ass = kwargs.pop('ass')
		super(SaveAsCSVAssessment,self).__init__(*args,**kwargs)
		self.fields['Module'].widget = forms.HiddenInput(attrs={'value' : self.mod})
		self.fields['AssID'].widget = forms.HiddenInput(attrs={'value' : self.ass})
		
class SaveAsPDFStudent(forms.Form):
	Upid = forms.CharField(required=False)
	AssID = forms.CharField(required=False)
	Module = forms.DateField(required=False)
	def __init__(self,*args,**kwargs):
		self.id = kwargs.pop('id')
		self.mod = kwargs.pop('mod')
		self.ass = kwargs.pop('ass')
		super(SaveAsPDFStudent,self).__init__(*args,**kwargs)
		self.fields['Upid'].widget = forms.HiddenInput(attrs={'value' : self.id})
		self.fields['Module'].widget = forms.HiddenInput(attrs={'value' : self.mod})
		self.fields['AssID'].widget = forms.HiddenInput(attrs={'value' : self.ass})

class SaveAsCSVStudent(forms.Form):
	Upid = forms.CharField(required=False)
	AssID = forms.CharField(required=False)
	Module = forms.DateField(required=False)
	def __init__(self,*args,**kwargs):
		self.id = kwargs.pop('id')
		self.mod = kwargs.pop('mod')
		self.ass = kwargs.pop('ass')
		super(SaveAsCSVStudent,self).__init__(*args,**kwargs)
		self.fields['Upid'].widget = forms.HiddenInput(attrs={'value' : self.id})
		self.fields['Module'].widget = forms.HiddenInput(attrs={'value' : self.mod})
		self.fields['AssID'].widget = forms.HiddenInput(attrs={'value' : self.ass})
		
class SaveAsPDF(forms.Form):
	Upid = forms.CharField(required=False)
	Module = forms.CharField(required=False)
	DateFrom = forms.DateField(required=True)
	DateTo = forms.DateField(required=True)
	Table = forms.CharField(required=False)
	def __init__(self,*args,**kwargs):
		self.id = kwargs.pop('id')
		self.mod = kwargs.pop('mod')
		self.datefrom = kwargs.pop('datefrom')
		self.dateto = kwargs.pop('dateto')
		self.table = kwargs.pop('table')
		super(SaveAsPDF,self).__init__(*args,**kwargs)
		self.fields['Upid'].widget = forms.HiddenInput(attrs={'value' : self.id})
		self.fields['Module'].widget = forms.HiddenInput(attrs={'value' : self.mod})
		self.fields['DateFrom'].widget = forms.HiddenInput(attrs={'value' : self.datefrom})
		self.fields['DateTo'].widget = forms.HiddenInput(attrs={'value' : self.dateto})
		self.fields['Table'].widget = forms.HiddenInput(attrs={'value' : self.table})
		
class SaveAsCSV(forms.Form):
	Upid = forms.CharField(required=False)
	Module = forms.CharField(required=False)
	DateFrom = forms.DateField(required=True)
	DateTo = forms.DateField(required=True)
	Table = forms.CharField(required=False)
	def __init__(self,*args,**kwargs):
		self.id = kwargs.pop('id')
		self.mod = kwargs.pop('mod')
		self.datefrom = kwargs.pop('datefrom')
		self.dateto = kwargs.pop('dateto')
		self.table = kwargs.pop('table')
		super(SaveAsCSV,self).__init__(*args,**kwargs)
		self.fields['Upid'].widget = forms.HiddenInput(attrs={'value' : self.id})
		self.fields['Module'].widget = forms.HiddenInput(attrs={'value' : self.mod})
		self.fields['DateFrom'].widget = forms.HiddenInput(attrs={'value' : self.datefrom})
		self.fields['DateTo'].widget = forms.HiddenInput(attrs={'value' : self.dateto})
		self.fields['Table'].widget = forms.HiddenInput(attrs={'value' : self.table})	


class FilterAuditLog(forms.Form):
	Date_From = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'e.g. 2014-04-23 15:00', 'class': 'datepicker'}), required=True)
	Date_To = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'e.g. 2014-04-24 16:00', 'class': 'datepicker'}), required=True)
	Table = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Person'}), required=False)
	up_ID = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 12345678'}), max_length=8, required=False)
	Module = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. COS301'}), max_length=6, required=False)
	

def getStudentModules(request):
	person = getSessionPerson(request)
	return person.studentOf
	
class Modules(forms.Form):
	Select_Module = forms.ChoiceField()
	def __init__(self,*args,**kwargs):
		self.req = kwargs.pop('req')
		super(Modules,self).__init__(*args,**kwargs)
		self.fields['Select_Module'] = forms.ChoiceField(widget = forms.Select(), choices=[(x, x) for x in getStudentModules(request=self.req)], required = True,)
		
def getAllAssessmentsStudent(request, module):
	assessments = []
	person = getSessionPerson(request)
	ass = getAllAssementsForStudent(person.upId, module)
	for assessment in ass:
		assessments.append(assessment.getName())
	#assessments = ['Exam', 'Semester Tests', 'Practicals', 'Tutorials', 'Class Tests']
	return assessments
	
class Assessments(forms.Form):
	Select_Assessment = forms.ChoiceField()
	Module = forms.CharField()
	def __init__(self,*args,**kwargs):
		self.mod = kwargs.pop('mod')
		self.req = kwargs.pop('req')
		super(Assessments,self).__init__(*args,**kwargs)
		self.fields['Module'].widget = forms.HiddenInput(attrs={'value' : self.mod})
		self.fields['Select_Assessment'] = forms.ChoiceField(widget = forms.Select(), choices=[(x, x) for x in getAllAssessmentsStudent(request=self.req, module=self.mod)], required = True,)
		
def getLecturerModules(request):
	person = getSessionPerson(request)
	return person.lectureOf
	
class LecturerModules(forms.Form):
	Select_Module = forms.ChoiceField()
	def __init__(self,*args,**kwargs):
		self.req = kwargs.pop('req')
		super(LecturerModules,self).__init__(*args,**kwargs)
		self.fields['Select_Module'] = forms.ChoiceField(widget=forms.Select(), choices=[(x, x) for x in getLecturerModules(request=self.req)], required=True)

def getAllAssessments(module):
	assessments = []
	ass = getAllAssessmentsForModule(module)
	for assessment in ass:
		assessments.append(assessment.getName())
	#assessments = ['Exam', 'Semester Tests', 'Practicals', 'Tutorials', 'Class Tests']
	return assessments
	
class AssessmentsLecturer(forms.Form):
	Select_Assessment = forms.ChoiceField()
	Module = forms.CharField()
	def __init__(self,*args,**kwargs):
		self.mod = kwargs.pop('mod')
		super(AssessmentsLecturer,self).__init__(*args,**kwargs)
		self.fields['Module'].widget = forms.HiddenInput(attrs={'value' : self.mod})
		self.fields['Select_Assessment'] = forms.ChoiceField(widget = forms.Select(), choices=[(x, x) for x in getAllAssessments(module=self.mod)], required = True,)
	
	
'''
    REPORTING FUNCTIONS
'''

def renderCSV(request):
	try:
		P = getSessionPerson(request)	
		person = getPersonByID(request.POST['studentID'])
	
	
		nform = RenderForm() 
		if request.method == 'POST':

		  form = RenderForm(request.POST) # A form bound to the POST data
  
		  if form.is_valid():
		  
		    outputType = form.cleaned_data['outputType']
		    assessment = form.cleaned_data['assessment']	
		    module = form.cleaned_data['module']
		    userID = form.cleaned_data['userID']
		    alteredTable = form.cleaned_data['alteredTable']
		    dateFrom = form.cleaned_data['dateFrom']
		    dateTo = form.cleaned_data['dateTo']
	except:
		return render(request,'Reporting_Main.html', {'form': nform,  'msg':"Please Log In"})
		
def renderPDF(request): 
	try:
		P = getSessionPerson(request)	
		person = getPersonByID(request.POST['studentID'])
	
			
		nform = RenderForm() 
		if request.method == 'POST':
		  form = RenderForm(request.POST) # A form bound to the POST data

		  if form.is_valid():

		    outputType = form.cleaned_data['outputType']
		    assessment = form.cleaned_data['assessment']
		    module = form.cleaned_data['module']
		    userID = form.cleaned_data['userID']
		    alteredTable = form.cleaned_data['alteredTable']
		    dateFrom = form.cleaned_data['dateFrom']
		    dateTo = form.cleaned_data['dateTo']
		  
		    try:
			    pdfGen = PDFReportGenerator()
			    type = request.POST['type']
			    if type == "ass" :
				    report =  pdfGen.generateReport(self,  request.POST['mod_code'], assessment, outputType) #Assessment Report
				    return render(request, report,'Reporting_Main.html', {'person': P}) # Redirect after POST

			    elif type == "stu" :
				    report =  pdfGen.generateReport(self,  request.POST['mod_code'], P.getID(), assessments, outputType)  #Student Marks Report

			    else:#type == 'aud'
				    report =  pdfGen.generateReport(self,  request.POST['mod_code'], P.getID(), alteredTable, dateFrom, dateTo, outputType) 

		    except Exception, e:
				    return render(request,'Reporting_Main.html', {'form': nform, 'msg':"Session ERROR"})	
	
		else:	
			return render(request,'Reporting_Main.html', {'form': nform},{'pdf' : report})
	except:
		return render(request,'Reporting_Main.html', {'form': nform,  'msg':"Please Log In"})

def viewAssessments(request, mod_code):
	try:
		P = getSessionPerson(request)
		Assessments = getAllAssessmentsForModule(mod_code)
		return render(request,'div.html', {'Assessments': Assessments})		
	except:
		return render(request,'login.html', {'form': nform,  'msg':"Please login"})

def save_as_pdf_assessment(request):
	if request.method == 'POST':
		Module = request.POST['Module']
		AssID = request.POST['AssID']
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="AssessmentReport.pdf"'
		reportGenerator = PDFReportGenerator()
		testReport = reportGenerator.generateAssessmentReport(Module, AssID, response)
		return response
		#p = canvas.Canvas(response)
		#p.drawString(3, 3, "Look mommy I can download a PDF file :)")
		#p.showPage()
		#p.save()
		#return response
		
def save_as_csv_assessment(request):
	if request.method == 'POST':
		Module = request.POST['Module']
		AssID = request.POST['AssID']
		reportGenerator = CSVReportGenerator()
		testReport = reportGenerator.generateAuditReport(Module, AssID)
		response = HttpResponse(testReport, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="AssessmentReport.csv"'
		return response
		#response = HttpResponse('COS301, StudentMarks, 30, 40, 60','text/csv')
		#response['Content-Disposition'] = 'attachment; filename="StudentReport.csv"'
		#return response
		
def save_as_pdf_student(request):
	if request.method == 'POST':
		upID = request.POST['Upid']
		Module = request.POST['Module']
		AssID = request.POST['AssID']
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="StudentReport.pdf"'
		reportGenerator = PDFReportGenerator()
		testReport = reportGenerator.generateStudentMarksReport(Module, upID, AssID, response)
		return response
		#p = canvas.Canvas(response)
		#p.drawString(3, 3, "Look mommy I can download a PDF file :)")
		#p.showPage()
		#p.save()
		#return response
		
def save_as_csv_student(request):
	if request.method == 'POST':
		upID = request.POST['Upid']
		Module = request.POST['Module']
		AssID = request.POST['AssID']
		reportGenerator = CSVReportGenerator()
		testReport = reportGenerator.generateStudentMarksReport(Module, upID, AssID)
		file_to_send = ContentFile(testReport)
		response = HttpResponse(testReport,'application/csv')
		response['Content-Disposition'] = 'attachment; filename="StudentReport.csv"'
		return response 
		#response = HttpResponse('COS301, StudentMarks, 30, 40, 60','text/csv')
		#response['Content-Disposition'] = 'attachment; filename="StudentReport.csv"'
		#return response
		
def save_as_pdf(request):
	if request.method == 'POST':
		upID = request.POST['Upid']
		Module = request.POST['Module']
		DateFrom = request.POST['DateFrom']
		DateTo = request.POST['DateTo']
		Table = request.POST['Table']
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="AuditReport.pdf"'
		reportGenerator = PDFReportGenerator()
		testReport = reportGenerator.generateAuditReport(Module, upID, Table, DateTo, DateFrom, response)	
		return response
		#p = canvas.Canvas(response)
		#p.drawString(3, 3, "Look mommy I can download a PDF file :)")
		#p.showPage()
		#p.save()
		#return response
	
def save_as_csv(request):
	if request.method == 'POST':
		upID = request.POST['Upid']
		Module = request.POST['Module']
		DateFrom = request.POST['DateFrom']
		DateTo = request.POST['DateTo']
		Table = request.POST['Table']
		reportGenerator = CSVReportGenerator()
		testReport = reportGenerator.generateAuditReport(Module, upID, Table, DateTo, DateFrom)
		response = HttpResponse(testReport,'text/csv')
		return reponse
		#response = HttpResponse('COS301, StudentMarks, 30, 40, 60','text/csv')
		#response['Content-Disposition'] = 'attachment; filename="AuditReport.csv"'
		#return response
	
def audit_report(request):
	if request.method == 'POST':
		form = FilterAuditLog(request.POST)
		if form.is_valid():
			DateFrom = form.cleaned_data['Date_From']
			DateTo = form.cleaned_data['Date_To']
			upId = form.cleaned_data['up_ID']
			table = form.cleaned_data['Table']
			module = form.cleaned_data['Module']
			auditReport = renderAuditReport(module, upId, table, DateFrom, DateTo)
			#auditReport = '<div><h1>Test report</h1><table><tr><th>Date</th><th>Details</th></tr><tr><td>2014-04-14</td><td>Wrote rendering class</td></tr><tr><td>2014-04-14</td><td>Created Test Audit Log</td></tr><tr><td>2014-04-14</td><td>Inserted Test Data</td></tr><tr><td>2014-04-14</td><td>I hope this works</td></tr><tr><td>2014-04-14</td><td>How do you import classes?</td></tr><tr><td>2014-04-14</td><td>__init__</td></tr><tr><td>2014-04-14</td><td>If you see this then it worked</td></tr></table></div>'
			PDFForm = SaveAsPDF(id=upId, mod=module, datefrom=DateFrom, dateto=DateTo, table=table)
			CSVForm = SaveAsCSV(id=upId, mod=module, datefrom=DateFrom, dateto=DateTo, table=table)
			form = FilterAuditLog()
			return render(request, 'auditReport.html', {'form': form, 'auditReport' : auditReport, 'DateFrom' : DateFrom, 'DateTo' : DateTo, 'upId' : upId, 'table' : table, 'module' : module, 'PDFForm' : PDFForm, 'CSVForm' : CSVForm})
		else:	
			return render(request, 'auditReport.html', {'form': form})
	else:
		form = FilterAuditLog() 
		return render(request, 'auditReport.html', {'form': form})

def assessment_report(request):
	if request.method == 'POST':
		module = request.POST['Select_Module']
		form = AssessmentsLecturer(mod=module)
		return render(request, 'assessmentReport.html', {'formAssessments': form, 'name' : 'Assessments', 'module' : module})
	else:
		form = LecturerModules(req=request)
		return render(request, 'assessmentReport.html', {'formModules' : form, 'name' : 'Modules'})

def student_report(request):
	if request.method == 'POST':
		module = request.POST['Select_Module']
		form1 = form = Modules(req=request)
		form2 = Assessments(mod=module, req=request)
		return render(request, 'studentReport.html', {'formModules' : form1, 'formAssessments': form2, 'name' : 'Assessments', 'module' : module})
	else:	
		form = Modules(req=request)
		return render(request, 'studentReport.html', {'formModules' : form, 'name' : 'Modules'})
		
def assessment_report_leaf_assessments(request):
	if request.method == 'POST':
		ass = request.POST['Select_Assessment']
		module = request.POST['Module']
		form = AssessmentsLecturer(mod=module)
		now = datetime.datetime.utcnow().replace(tzinfo=utc)
		assessment = getAssessmentForModuleByName(module, ass)
		assessmentID = assessment[0].id
		assessmentReportOutput = renderAssessmentReport(module, assessmentID)
		PDFForm = SaveAsPDFAssessment(mod=module, ass=assessmentID)
		CSVForm = SaveAsCSVAssessment(mod=module, ass=assessmentID)
		#PDFForm = SaveAsPDFAssessment(mod='COS301', ass='11')
		#CSVForm = SaveAsCSVAssessment(mod='COS301', ass='11')
		#assessmentReportOutput = '<div><h2>Stats</h2><br/><b>Student Marks </b><table><tr><th>Student No</th><th>ST1</th><th>ST2</th><th>T1</th><th>T2</th></tr><tr><td> Mean </td><td>0</td><td>45.0</td><td>50.0</td><td>5.0</td></tr></table><br/><table><tr><td> Total marks </td><td>50</td><td>50</td><td>10</td><td>10</td></tr><tr><th>Student No</th><th>ST1</th><th>ST2</th><th>T1</th><th>T2</th></tr><tr><td>10122893</td><td>45</td><td>50</td><td>5</td><td>10</td></tr><tr><td>10392837</td><td>45</td><td>50</td><td>5</td><td>10</td></tr><tr><td>12748392</td><td>45</td><td>50</td><td>5</td><td>10</td></tr></table><br/><div>'
		return render(request, 'assessmentReport.html', {'formAssessments' : form, 'name' : 'Assessments', 'assessmentName' : ass, 'assessmentReportOutput' : assessmentReportOutput, 'now' : now, 'PDFForm' : PDFForm, 'CSVForm' : CSVForm})
	else:
		form = LecturerModules(req=request)
		return render(request, 'assessmentReport.html', {'formModules' : form, 'name' : 'Modules'})
	
def student_report_leaf_assessments(request):
	if request.method == 'POST':
		ass = request.POST['Select_Assessment']
		module = request.POST['Module']
		form = Assessments(mod=module, req=request)
		now = datetime.datetime.utcnow().replace(tzinfo=utc)
		person = getSessionPerson(request)
		studentId = person.upId
		assessment = getAssessmentForModuleByName(module, ass)
		assessmentID = assessment[0].id
		studentReportOutput = renderStudentReport(module, studentId, assessmentID)
		PDFForm = SaveAsPDFStudent(id=studentId, mod=module, ass=assessmentID)
		CSVForm = SaveAsCSVStudent(id=studentId, mod=module, ass=assessmentID)
		#PDFForm = SaveAsPDFStudent(id='12147100', mod='COS301', ass='11')
		#CSVForm = SaveAsCSVStudent(id='12147100', mod='COS301', ass='11')
		#studentReportOutput = '<div><h1>COS332 Student Marks Report for 10189337 </h1><table><tr><td>Assessment </td><th>ST1</th><th>ST2</th><th>P1</th><th>P2</th><th>P3</th></tr><tr><td> Total marks </td><td>50</td><td>50</td><td>10</td><td>10</td><td>10</td></tr><tr><td>Student Mark</td><td>23</td><td>45</td><td>3</td><td>7</td><td>9</td></tr></table><br/></div>'
		return render(request, 'studentReport.html', {'formAssessments' : form, 'name' : 'Assessments', 'assessmentName' : ass, 'studentReportOutput' : studentReportOutput, 'now' : now, 'PDFForm' : PDFForm, 'CSVForm' : CSVForm})
	else:	
		form = Modules(req=request)
		return render(request, 'studentReport.html', {'formModules' : form, 'name' : 'Modules'})

'''
    END REPORTING FUNCTIONS
'''

'''COLLEN'''
def get_all_modules_lecture(request):
	person = getSessionPerson(request)
	modules  = getAllModulesForLecturer(person.upId)
	return render(request, 'marks-management.html', {'modules': modules})

def get_all_modules_marker(request):
	person = getSessionPerson(request)
	modules  = getAllModulesForMarker(person.upId)
	return render(request, 'marks-management.html', {'modules': modules})

def get_all_students_of_module():
	module_code = request.POST['mod_code']
	students = getAllStudentsOfModule(module_code)
	return render(request, 'marks-management.html', {'students': students})

'''END COLLEN'''

'''MARTIN'''
def AssessmentManager(request):
	if request.method == 'POST':
		form = AssessmentManagerForm(request.POST)
		if form.is_valid():
			course = forms.cleaned_data['course']
			assessmentType = forms.cleaned_data['Assessment_Type']
			assessmentDetails = forms.cleaned_data['assessmentDetails']
			totalMark = forms.cleaned_data['totalMark']
			markWeight = forms.cleaned_data['Mark_Weight']
			assessmentName = forms.cleaned_data['Assessment_Name']
			moduleId = forms.cleaned_data['moduleId']
			assessmentId = forms.cleaned_data['assessmentId']
			insertAssessment(assessmentId,assessmentName,markWeight,assessmentType,moduleId)
			return render(request, 'assessmentManager.html', {'msg': "Assessment Inserted"}) # Redirect after POST
		else:
		  return render(request, 'assessmentManager.html', {'form': form, 'msg': form.errors})
	else:
	  P = getSessionPerson(request)	  
	  form = AssessmentManagerForm() 
	  return render(request, 'assessmentManager.html', {'form': form, 'Courses' : P.lectureOf})

def lecturer_assessment(request):
	return render(request, 'lecturerAssessment.html')
'''END MARTIN'''

	
	
def publish(request):
	if request.method == 'POST': 
	  try:    
	    csvfile = request.FILES['csvFile']
	    parseMarksToDB(request, csvfile)
	    return render(request, 'publish.html', {'msg' : "Marks Published!"})
	  except IOError, e:
	    return render(request, 'publish.html', {'msg' : "Unable to open the file!"})
	else:
	  return render(request, 'publish.html', {})
	
	
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
        return render(request, 'login.html', {}, context)
