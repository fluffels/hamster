import json
from django.test import TestCase
#from djnago.utils import simplejson as json

class WebServiceTest(TestCase) :			
	def Login(self):
		url = '/Android/User/login'
		payload = {
			"uid" : "u89000999",
			"pwd" : "Aram"
		}
		json_block = json.dumps(payload)
		response = self.client.post(url, json_block, content_type = 'application/json')
		response_data = json.loads(response.content)
		print(response_data)
		
	def getAllMarksForModule(self):
		url = '/Android/Student/getAllMarksForModule'
		payload = {
			"uid" : "u89000999",
			"module" : "COS301"
		}
		json_block =json.dumps(payload)
		response = self.client.post(url, json_block, content_type = 'application/json')
		response_data = json.loads(response.content)
		print(response_data)
	
	def getStudentsToMark(self):
		url = '/Android/Marker/getStudentsToMark'
		payload = {
			"uid" : "u89000999",
			"module" : "COS301",
			"assessmentID" : "P1"
		}
		json_block =json.dumps(payload)
		response = self.client.post(url, json_block, content_type = 'application/json')
		response_data = json.loads(response.content)
		print(response_data)

	def saveMarks(self):
		url = '/Android/Marker/saveMarks'
		payload = {
			"uid" : "u89000999",
			"module" : "COS301",
			"leadAssessmentID" : "P1",
			"mark" : 58
		}
		json_block =json.dumps(payload)
		response = self.client.post(url, json_block, content_type = 'application/json')
		response_data = json.loads(response.content)
		print(response_data)

	def getTaskListByAssessment(self):
		url = '/Android/Marker/getTaskListByAssessment'
		payload = {
			"module" : "COS301",
			"AssessmentName" : "P1",
			"sUID": "u89000999"
		}
		json_block =json.dumps(payload)
		response = self.client.post(url, json_block, content_type = 'application/json')
		response_data = json.loads(response.content)
		print(response_data)

	def getActiveAssessments(self):
		url = '/Android/Marker/getActiveAssessments'
		payload = {
			"module" : "COS301"
		}
		json_block =json.dumps(payload)
		response = self.client.post(url, json_block, content_type = 'application/json')
		response_data = json.loads(response.content)
		print(response_data)

	def logout(self):
		url = '/Android/User/logout'
		response = self.client.post(url)
		response_data = json.loads(response.content)
		print(response_data)


	def all(self):
		print "Logging Test:"
		WebServiceTest.Login(self)

		print ""
		print ""

		print "getAllMarksForModule"
		WebServiceTest.getAllMarksForModule(self)

		print ""
		print ""

		print "getStudentsToMark"
		WebServiceTest.getStudentsToMark(self)


		print ""
		print ""

		print "saveMarks"
		WebServiceTest.saveMarks(self)

		print ""
		print ""

		print "getTaskListByAssessment"
		WebServiceTest.getTaskListByAssessment(self)

		print ""
		print ""

		print "getActiveAssessments"
		WebServiceTest.getActiveAssessments(self)

		print ""
		print ""

		print "logout"
		WebServiceTest.logout(self)