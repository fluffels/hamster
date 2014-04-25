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
			markAlloc =BL.getMarkAllocationFromID(leafAssessmentID)
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

def getStudents(request):
	if request.method == 'GET':
		try:
			#json_data =json.loads(request.body)
			assessmentID = request.GET["assessmentID"]
			print request.session['user']
			marker =BL.getSessionPerson(request)
			openSessions = BL.getOpenSessionsForMarker(assessmentID,marker.upId[0])
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
