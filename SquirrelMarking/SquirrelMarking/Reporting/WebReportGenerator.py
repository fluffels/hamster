
from ReportGenerator import ReportGenerator
from Report import Report
from AuditReport import AuditReport
from StudentMarksReport import StudentMarksReport
from AssessmentReport import AssessmentReport
from SquirrelMarking.businessLogicAPI import *

class WebReportGenerator(ReportGenerator):
  def __init__(self):		#Constructor
    test = ""
   
 #api 
#getAllAssessmentTotalsForStudent(uid, mod_code)
# getLeafAssessmentMarksOfAsssessmentForStudent(uid, assess_id)
#getAssessmentTotalForStudent(uid, mod_code, assess_id)
#getAllAssementsForStudent(empl_no,mod_code)
#getAllStudentsOfModule(mod_code)
  def generateAssessmentReport(self, module, assessment): #Assessment Report

	returnData =[]
	name = []
	total = []
	mark = []


	people = getAllStudentsOfModule(module)
	for x in people:
		tempList = []
		tempList.append(x.getupId())
		tempData = getAssessmentTotalForStudent(x.getupId(),module,assessment)
		for y in tempData:
			tempList.append(y[2])
		returnData.append(tempList)
	        
	tempData = getAssessmentTotalForStudent(people[0].getupId(),module,assessment)
	for y in tempData:
		name.append(y[0])
		total.append(y[1])
	reportName = module + " Assessment Report"
	#~ getAllAssessmentTotalsForStudent
	#~ headings = ["Student No", "ST1", "ST2", "T1", "T2"]
	#~ totals = [50, 50, 10, 10]
	#~ returnedData = [["10122893", 45, 50, 5, 10], ["10392837", 45, 50, 5, 10], ["12748392", 45, 50, 5, 10]]
	report = AssessmentReport(reportName, name, total, returnData)
	return report
  #--------------------------------------------------------------------------------------------------
  
  def generateStudentMarksReport(self, module, studentNo, assessments):  #Student Marks Report
                    
	tempData = getAllAssessmentTotalsForStudent(studentNo,module)


	name = []
	total = []
	mark = []

	for x in tempData:
		name.append(x[0])
		total.append(x[1])
		mark.append(x[2])



	#studentNumber = "10189337"
	#_module = "COS332"
	reportName = module + " Student Marks Report for " + studentNo 
	#headings = ["ST1", "ST2", "P1", "P2", "P3"]
	#totals = [50, 50, 10, 10, 10]
	#returnedData = [23, 45, 3, 7, 9]


	"""
	#This part can be uncommented once BusinessLogic provides the functions called below

	BLogicObject = businessLogicAPI()
	studentNumber = studentNo
	_module = module


	if assessments == "":
	    totals = BLogicObject.getTotals(_module)
	    returnedData = BLogicObject.getStudentMarks(_module, studentNumber)
	else:
	    totals = BLogicObject.getTotals(_module, assessments)
	    returnedData = BLogicObject.getStudentMarks(_module, studentNumber)
	"""
	report = StudentMarksReport(reportName, name, total, mark)
	return report


  def generateAuditReport(self, module, userID, alteredTable, dateFrom, dateTo):  #Audit Report
	reportName = module + " Audit Report for "
	name = ""
	data = ""
	print userID
	headings =  reportName
	if module != "":
		
		if userID != "":
			
			if alteredTable != "":
				data = getUserTableAudit(module,userID,alteredTable,dateFrom,dateTo)
			else:
				data = getAuditLogFromTimeRangeAndUser(userID,dateFrom,dateTo) 
		else:
			if alteredTable != "":
				data = getTableAudit(module,alteredTable,dateFrom,dateTo)
	print data
	for x in data:
		print "t"
	
	report = AuditReport(reportName, headings, data)
	return report
