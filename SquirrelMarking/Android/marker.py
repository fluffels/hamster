from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import SquirrelMarking.businessLogicAPI as BL
import json
	
def saveMarks(request):
	data = [
	{
		'type':-1,
		'message':'Request failed',
		'success':'false'
	}]
	if request.method == 'POST':
		try:
			json_data =json.loads(request.body)
			student = json_data['uid']
			course = json_data['courseCode']
			leafAssessmentID = json_data['leafAssessmentID']
			mark = json_data['mark']
			markAlloc =getMarkAllocationFromID(leafAssessmentID)
			BL.updateMarkAllocation(request, markAlloc, mark)
			
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

def getStudents(request):
	if request.method == 'POST':
		try:
			json_data =json.loads(request.body)
			assessmentID = json_data["assessmentID"]
			marker =BL.getSessionPerson(request)
			openSessions = BL.getOpenSessionsForMarker(assessmentID,marker)
			students = []

			for s in openSessions:
				st =BL.getStudentsForASession(s)
				for stu in st:
					students.append(stu)

			data = [
			{
				'type':1,
				'message':'Mark saved',
				'students':students
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

def getTaskListByAssessment(request):
	data =[{
		'type' :-1,
		'message':'Error in request'
	}]
	if request.method == 'POST':
		try:
			json_data =json.loads(request.body)
			module =json_data['module']
			assessmentID =json_data['assessmentID']
			suid =json_data['studentuid']

			assessment =BL.getAssessmentFromID(assessmentID)

			LeafAssessments =BL.getAllLeafAssessmentsForAssessment(assessment)
			leafName =[]
			maxMark =[]
			currentMark =[]
			leafID =[]
			for lAssessment in LeafAssessments:
				mark =BL.getMarkAllocationForLeafAssessmentOfStudent(uid, lAssessment)
				maxMark.append(lAssessment.getMax_mark())
				currentMark.append(mark.getMark())
				leafID.append(mark.getID())
				leadName.append(lAssessment.getName())

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
			data =[{
				'type':-1,
				'message':'Request failed'
			}]
			return HttpResponse(json.dumps(data))
	else:
		return HttpResponse(json.dumps(data))
		
def getActiveAssessments(request):
	data =[{
		'type' :-1,
		'message':'Error in request'
	}]
	if request.method == 'POST':
		json_data =json.loads(request.body)
		module = json_data['module']
		assessments = BL.getAllOpenAssessmentsForModule(module)
		assessment =[]
		AssessmentName = []
		Id = []
			
		for assessment in assessments:
			AssessmentName.append(assessment.getName())
			ID.append(assessment.getID())
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
