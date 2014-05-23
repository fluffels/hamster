from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import SquirrelMarking.businessLogicAPI as BL
import json

def getAllMarksForModule(request):
	#json_data =json.loads(request.body)
	studentNumber = request.GET['uid']
	module = request.GET['module']
	assessments = BL.getAllAssessmentTotalsForStudent(studentNumber,module)
	AssessmentName = []
	mark = []
	total = []
		
	for assessment in assessments:
		print assessment
		AssessmentName.append(assessment[0])
		total.append(assessment[1])
		mark.append(assessment[2])
	data = [
		{
			'type':1,
			'message':'success',
			'Assessment_Name':AssessmentName,
			'Acquired_Mark':mark,
			'Total_Mark':total
		}
	]
	ret = HttpResponse(json.dumps(data))
	return ret
	
def getModules(request):
	if request.method == 'GET':
		#json_data = json.loads(request.body)
		student =request.GET['uid']
		moduleObjects = BL.getAllModulesForStudent(student)
		print moduleObjects
		modules = []
		for module in modules:
			modules.append(moduleObjects.getModuleCode())
		data  = [
			{
				'type':1,
				'message':'success',
				'modules':modules
			}
		]
		ret = HttpResponse(json.dumps(data))
		return ret
	else:
		raise Http404()

def getMark(request):
	if request.method == 'GET':
		#json_data = json.loads(request.body)
		student = request.GET['uid']
		module = request.GET['module']
		
		#business logic will provide mark for this particular module
		#mark = BL.getMark(student, module)
		data  = [
		{
			'type':-1,
			'message':'this did not work'
		}
		]
		for l in MODULES:
			if l[0] == module:
				data  = [
				{
					'type':1,
					'message':'success',
					'marks':l[1]
				}
				]
		ret = HttpResponse(json.dumps(data))
		return ret
	else:
		raise Http404()


#getAssesmentForModule
	#in
		#
	#out
		#mod code
		#ass nom
		#ass mark
		#total

def getModuleMarks(request):
	if request.method == 'GET':
		#json_data = json.loads(request.body)
		student = request.GET['uid']
		data = [
			{
				'type' : 1,
				'module' : "COS344"
			}
		]
		return HttpResponse(json.dumps(MODULES))
	else:
		raise Http404()