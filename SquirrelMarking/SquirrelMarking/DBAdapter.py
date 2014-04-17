import csv
import time
import webbrowser
import datetime
from businessLogicAPI import *

def parseMarksToDB(request,csvFile):
	#try:
		reader = csv.reader(csvFile, delimiter=',')
		ts = time.time()
		time_stamp = st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		for row in reader:
			student = row[0]
			sessionId = row[1]
			mark = row[2]
			marker = row[3]
			module = row[4]
			assessment = row[5]
			leafAssessment = row[6]
			leafAssessmentID = row[7]
			print row
			#Check if student is valid
			student_modules = getAllModulesForStudent(student)
			print student_modules
			print row[4]
			if module in student_modules:
				#Check is session exists
				sessions_module = getAllSessionsForModule(module)
				# check if session 
				if checkSessionList(sessions_module,sessionId):
					#Check of isLeaf
					list = getLeafAssessmentOfAssessmentForModuleByName(module,assessment,leafAssessment)
					if len(list) == 0:
						raise Exception('leaf does not exist')
						print 'leaf does not exist'
					else:
						
						alloc_id = createMarkAllocation(request,leafAssessmentID,sessionId,marker,student,time_stamp)
						updateMarkAllocation(request,alloc_id,mark)
				else:
					raise Exception('session does not exist')
					print 'session does not exist'
			else:
				raise Exception('not a student')
		
def checkSessionList(list,id):
	for row in list
		if row.getID() = id
			return true
	return false