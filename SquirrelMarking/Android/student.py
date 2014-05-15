from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import SquirrelMarking.businessLogicAPI as BL
import json

'''
Function: getAllMarksForModule
Description: This function gets all the marks of a student for a specific module

@type: String
@param: The http request containing the user ID and module for which marks are to be retireved

@type: String
@return: The http responce containing all the modules mark
'''
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
	
	
'''
Function: getModules
Description: Gets all the modules that the student is registered for

@type: String
@param: A http Get Request containing the student number

@type: String
@return: A http Responce containing the modules or a http error "page not found" if there student 
	     is not enrolled for any module
'''
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

'''
Function: getMark
Description: 
'''
def getMark(request):
	# this fucntion does not make any sence for me.....
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
'''
Function: getModuleMarks
Description: 
'''
def getModuleMarks(request):
	#this is hard coded and there's already a function that does this
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