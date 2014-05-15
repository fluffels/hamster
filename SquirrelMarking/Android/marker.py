from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import SquirrelMarking.businessLogicAPI as BL
import json
import datetime as datetime

'''
Function: saveMarks
Description: the function saves the mark of the leaf assessment of a certain module

@type: String
@param: A http request that contains the student number, the course code, the leafAssessment ID and the mark that is to be saved

@type: String
@return: A http responce confirming if the mark was saved or not 
'''
def saveMarks(request):
	data = [
	{
		'type':-1,
		'message':'Request failed',
		'success':'false'
	}]
	if request.method == 'GET':
		try:
			student = request.GET['uid']
			course = request.GET['courseCode']
			leafAssessmentID = request.GET['leafAssessmentID']
			mark = request.GET['mark']
			#json_data =json.loads(request.body)
			#student = json_data['uid']
			#course = json_data['courseCode']
			#leafAssessmentID = json_data['leafAssessmentID']
			#mark = json_data['mark']
			print student
			markerID = BL.getSessionPerson(request).upId[0]
			sess = BL.getSessionForStudentForAssessmentOfModule(student,leafAssessmentID,course)
			
			print "E"
			if not(BL.checkMarkAllocationExists(sess,student,BL.getLeafAssessmentFromID(leafAssessmentID))):
				BL.createMarkAllocation(request, leafAssessmentID,sess.id,markerID,student,datetime.datetime.now())
			markAlloc = BL.getMarkAllocationForLeafOfStudent(student,BL.getLeafAssessmentFromID(leafAssessmentID),sess)	
			BL.updateMarkAllocation(request, markAlloc.id, mark)

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

'''
Function: getStudents
Description: Gets all the student that the user(marker) is supposed to mark fo a certain session

@type: String
@param: A http request containing the assessmentId and the marker's ID(employee number)

@type: String
@return: A http responce containing the students data for that session and an error message if not successful
'''
def getStudents(request):
	if request.method == 'GET':
		try:
			#json_data =json.loads(request.body)
			assessmentID = request.GET["assessmentID"]
			print request.session['user']
			marker =BL.getSessionPerson(request)
			openSessions = BL.getOpenSessionsForMarker(assessmentID,marker.upId[0])
			
			students = []
			stuNames = []
			stuSurnames = []
			stuIds = []

			for s in openSessions:
				st =BL.getStudentsForASession(s)
				for stu in st:
					students.append(stu)

			studentPersonList = BL.getPersonListFromArrayList(students)

			for studentItem in studentPersonList:
				stuIds.append(studentItem.upId) #should be stuIds.append(studentItem.getupId()) instead. But getupId return incorrect data
				stuNames.append(studentItem.firstName) #should be stuIds.append(studentItem.getfirstName()) instead. But studentItem.getfirstName() return incorrect data
				stuSurnames.append(studentItem.surname) #should be stuIds.append(studentItem.getsurname()) instead. But studentItem.getupsurname() return incorrect data
			print(stuIds)
			print(stuNames)
			print(stuSurnames)
			data = [
			{
				'type':1,
				'message':'Retrieving student details',
				#'students':students,
				'uid':stuIds,
				'name':stuNames,
				'surname':stuSurnames
			}]
			return HttpResponse(json.dumps(data))
		except Exception, e:
			data = [
			{
				'type':-1,
				'message':'Failed to get students. Server exception'
			}]
			return HttpResponse(json.dumps(data))
	else:
		raise Http404()
'''
Function: getTaskListByAssessment
Description: Gets all the leaf Assessment of an assessment for a specific module

@type: String
@param: A http request containing the module, assessment and  student number for the leafAssessment required

@type: String
@return: A http responce containing the leaf Assessment and its marks and an error message of not successful
'''
def getTaskListByAssessment(request):
	data =[{
		'type' :-1,
		'message':'Error in request'
	}]
	if request.method == 'GET':
		try:
			#json_data =json.loads(request.body)
			module =request.GET['module']
			assessmentID =request.GET['assessmentID']
			uid =request.GET['studentuid']

			assessment =BL.getAssessmentFromID(assessmentID)

			LeafAssessments =BL.getLeafAssessmentMarksOfAsssessmentForStudent(uid, assessmentID)
			print LeafAssessments
			leafName =[]
			maxMark =[]
			currentMark =[]
			leafID =[]
			for lAssessment in LeafAssessments:
				
				leafName.append(lAssessment[0])
				maxMark.append(lAssessment[1])
				currentMark.append(lAssessment[2])
				leafID.append(lAssessment[3])

			data =[{
				'type' :1,
				'message':'Getting all details for module requested',
				'taskName':leafName,
				'currentMark':currentMark,
				'maxMark':maxMark,
				'leadID':leafID
			}]
			return HttpResponse(json.dumps(data))
		except Exception ,e:
			raise e
			data =[{
				'type':-1,
				'message':'Request failed'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return HttpResponse(json.dumps(data))
		

'''
Function: getActiveAssessments
Description: The function gets all the assessment of a certain module

@type: String
@param: A http request containing the module whose assessment are to be retrieved

@type:String 
@return: A http responce containing the module's assessment and an error if it was unsuccessful 
'''
def getActiveAssessments(request):
	data =[{
		'type' :-1,
		'message':'Error in request'
	}]
	if request.method == 'GET':
		#json_data =json.loads(request.body)
		module = request.GET['module']
		assessments = BL.getAllOpenAssessmentsForModule(module)
		assessment =[]
		AssessmentName = []
		Id = []
			
		for assessment in assessments:
			AssessmentName.append(assessment.getName())
			Id.append(assessment.getID())
		data = [
			{
				'type':1,
				'message':'success',
				'assesmentName':AssessmentName,
				'assesmentID':Id
			}
		]
		ret = HttpResponse(json.dumps(data))
		return ret
	else:
		return HttpResponse(json.dumps(data))
