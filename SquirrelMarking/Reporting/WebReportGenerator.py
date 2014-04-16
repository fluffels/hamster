
from ReportGenerator import ReportGenerator
from Report import Report
from AuditReport import AuditReport
from StudentMarksReport import StudentMarksReport
from AssessmentReport import AssessmentReport
from SquirrelMarking.businessLogicAPI import *

class WebReportGenerator(ReportGenerator):
  def __init__(self):		#Constructor
    test = ""
   
  
  def generateAssessmentReport(self, module, assessment): #Assessment Report

	    reportName = module + " Assessment Report for "  + assessment
	    ge
	    getAllAssessmentTotalsForStudent
	    headings = ["Student No", "ST1", "ST2", "T1", "T2"]
	    totals = [50, 50, 10, 10]
	    returnedData = [["10122893", 45, 50, 5, 10], ["10392837", 45, 50, 5, 10], ["12748392", 45, 50, 5, 10]]
	    
	    """
	    #This part can be uncommented once BusinessLogic provides the functions called below
	    _module = module
	    
	    BLogicObject = businessLogicAPI()
	    totals = BLogicObject.getTotals(_module, assessments)
	    returnedData = BLogicObject.getAssessmentMarks(_module, assessments)
	    
	    """
	    
	    report = AssessmentReport(reportName, headings, totals, returnedData)
	    
	    return report;

                  
  #--------------------------------------------------------------------------------------------------
  
  def generateStudentMarksReport(self, module, studentNo, assessments, outputType):  #Student Marks Report
                    
            if outputType == "object":
                    

                    studentNumber = "10189337"
                    _module = "COS332"
                    reportName = _module + " Student Marks Report for " + studentNumber 
                    headings = ["ST1", "ST2", "P1", "P2", "P3"]
                    totals = [50, 50, 10, 10, 10]
                    returnedData = [23, 45, 3, 7, 9]
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
                    report = StudentMarksReport(reportName, headings, totals, returnedData)
                    return report
            else:
                    return "Error: Incorrect output type"


  def generateAuditReport(self, module, userID, alteredTable, dateFrom, dateTo, outputType):  #Audit Report
          
            if outputType == "object":
                 
                  
                    _module = module
                    _userID = userID
                    reportName = _module + " Audit Report for "
                    table = alteredTable
                    _dateFrom = dateFrom
                    _dateTo = dateTo
                    headings = ""
                    returnedData = ""
                    """
                    #This part can be uncommented once BusinessLogic provides the functions called below
                    
                    BLogicObject = businessLogicAPI()
                    if userID == "":
                            
                            returnedData = BLogicObject.getUserTableAudit(_module, table, _dateFrom, _dateTo)
                    elif table == "":
                            
                            returnedData = BLogicObject.getUserTableAudit(_module, _userID, _dateFrom, _dateTo)
                    else:
                            if _dateTo != "":
                                    import time
                                    _dateTo = time.strftime("%d/%m/%y")
                            returnedData = BLogicObject.getUserTableAudit(_module, _userID, table, _dateFrom,_dateTo) 
                 """
                    report = WebReport(reportName, headings, returnedData)
                    return report
            else:
                  return "Error: Incorrect output type"
