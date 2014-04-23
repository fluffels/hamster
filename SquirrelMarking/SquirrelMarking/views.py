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

def logout(request):
    try:
      login(request,"","")
    except:
      return loginWeb(request)
    
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

		
def viewAssessments(request):
	c = request.POST['mod_code']
	Assessments = getAllAssessmentsForModule(c)
	return render(request,'listAssessments.html', {'Assessments': Assessments, 'C': c})	

	
def viewAssessmentsOptions(request):
	c = request.POST['mod_code']
	print (c);
	Assessments = getAllAssessmentsForModule(c)
	print (Assessments);
	return render(request,'listAssessmentsOptions.html', {'Assessments': Assessments})	

def viewAssessmentSessionsOptions(request):
	c = request.POST['mod_code']
	a = request.POST['assess_id']
	P = getSessionPerson(request)
	#Sessions = getOpenSessionsForMarker(a, P.upId)
	Sessions = getOpenSessions(a)
	print (Sessions)
	return render(request,'listAssessmentSessionsOptions.html', {'Sessions': Sessions})
	
def getSessionStudentMarks(request):
	m = request.POST['mod_code']
	a = request.POST['assess_id']
	s = request.POST['sess_id']
	session = getSessionsFromID(s)
	students = getStudentsForASession(s)
	weight = session.assessment_id.assessment_weight
	class Student:
	    firstName = ""
	    upId = ""
	    surname = ""
	    total = ""
	    def __init__(self):
	      self.firstName = ""
	      self.upId = ""
	      self.surname = ""
	      self.total  = ""
	list = []
	for student in students:
	  stud = Student()
	  stud.firstName = student.firstName
	  stud.upId = student.upId
	  stud.surname = student.surname
	  stud.total = getAssessmentTotalForStudent(student.upId, m, a)
	  list.append(stud)
	print (Sessions)
	return render(request,'AssessmentStudentMarksTable.html', {'StudentMarks': list, 'weight' : weight})

def assessment_view(request):
    return render(request,'assessmentView.html', {'Assessments': assessmentName})	
	
def openAssessment(request, assessmentName):
	print (assessmentName)
	return render(request,'assessmentView.html', {'Assessments': assessmentName})	

def marks_management(request):
	P = getSessionPerson(request)
	modules = getAllModulesForMarker(P.upId)
	return render(request,'marks-management.html', {'modules': modules})	
	
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
				    return render_to_response(report,'Reporting_Main.html', {'person': P}) # Redirect after POST

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

# frequency analysis function to initialize variables	

def frequency_analysis(request):
        person = getSessionPerson(request)
        assessment = getAllAssementsForStudent(person.upId, getAllModulesForStudent(person.upId))
        return render(request, 'studentChosen.html', {'per': person, 'assessment' : assessment})

def getLeafAssessments(request):
        person = getSessionPerson(request)
        assess_id = request.POST['assess_id']
        x = getLeafAssessmentMarksOfAsssessmentForStudent(person.upId, assess_id)
        return render(request,  'studentChosen.html', {'leafAssessmentList' : x})
        
def  getAssessments(request):
        person = getPersonByID(request.POST['studentID'])
        leaf = request.POST['leafAssessment']
        if person == 'Empty':
            person = getSessionPerson(request)
        mode = request.POST['mode']
        if mode == 'Not Leaf':
            assessmentList = getAllLeafAssessmentsForAssessment(person.upId, leaf)
        else:
                assessmentList = getAllLeafAssessments(person.upId, leaf)
        type = request.POST['type']
        return render(request,  'studentChosen.html', {'per' : person, 'usrAllAssessments' : assessmentList, 'type' : type, 'leafAssesment' : leafAssesment })

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

def assessmentReport(request):
        t = get_template('assessmentReport.html')
        html = t.render(Context())
        return HttpResponse(html)

def studentModules(request):
        student = getSessionPerson(request)
        return render(request, 'studentChosen.html', {'modules' : student.getAllModulesForStudent()})
        
        
def getLecturerModules(request):
        lecturer = getSessionPerson(request)
        return render(request, 'assessmentReport.html', {'modules' : getAllModulesForLecturer(lecturer.upId)})
        
def searchStudents(request):
        searchedItemRequest = request.POST['searchedItem']
        studentSurnamesList = searchBySurname(searchedItemrequest) 
        studentNamesList = searchByName(searchedItemrequest)
        students = studentSurnamesList + studentNamesList
        return render(request, 'studentChosen.html', {'students' : students})
        
def displayStudent(request):
        person = getStudentByID(request.POST['upId'])
        return render(request, 'studentReport.html', {'person' : person})
        
def generate_auditLog(request):
        dateFrom = request.POST['dateFrom']
        dateTo = request.POST['dateTo']
        upId = request.POST['upId']
        if dateFrom is None and dateTo is None and upId is None:
            auditlog = getAuditLogFromID(upId) 
        elif dateFrom is None and dateTo is None and upId is not None:
            auditlog = getAuditLogFromTimeRange(dateFrom, dateTo) 
        return render(request, 'auditReport.html', {'auditlog' : auditlog})
        
        
def get_statistics(request):
        module = POST.request['module']
        frequencyAnalysisOfModule = getFrequencyAnalysis(module) #implement business logic function
        return render(request, 'stat.html', {'freqOfModule' : frequencyAnalysisOfModule, 'module' : module})

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
			assessmentType = forms.cleaned_data['assessmentType']
			assessmentDetails = forms.cleaned_data['assessmentDetails']
			totalMark = forms.cleaned_data['totalMark']
			markWeight = forms.cleaned_data['markWeight']
			assessmentName = forms.cleaned_data['assessmentName']
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
'''END MARTIN'''

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
