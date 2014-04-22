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
			student = row[2]
			sessionId = row[1]
			mark = row[3]
			marker = row[4]
			leafAssessmentID = row[0]
			
			if (not(checkLeafAssessmentExists(leafAssessmentID))):
				raise Exception("Leaf Assessment does not exist")
			if (not(checkSessionExists(sessionId))):
				raise Exception("Session does not exist")
			if (not(checkSessionBelongsToLeafAssessment(sessionId, leafAssessmentID))):
				raise Exception("Sessions does not belong to leaf assessment")
			if (not(isStudentInSession(sessionId, student))):
				raise Exception("Student not in session")
			if (not(isMarkerInSession(sessionId, marker))):
				raise Exception("Marker not in session")
			if (not(checkMarkAllocationExists(sessionId, student, leafAssessmentID))):
				raise Exception("Mark Allocation alredy exists")
				
			alloc_id = createMarkAllocation(request,leafAssessmentID,sessionId,marker,student,time_stamp)
			updateMarkAllocation(request,alloc_id,mark)
