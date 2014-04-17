from Reporting.AuditReport import AuditReport
from Reporting.AssessmentReport import AssessmentReport
from Reporting.StudentMarksReport import StudentMarksReport
from Reporting.PDFReportGenerator import *
from Reporting.CSVReportGenerator import *
from reportRenderers import *

#from reportRendering import AssessmentReportRending 

#TEST DATA - Assessment Report
name = "Assessment Report"
headings = ["Student No", "ST1", "ST2", "T1", "T2"]
totals = [50, 50, 10, 10]
returnedData = [["10122893", 45, 50, 5, 10], ["10392837", 45, 50, 5, 10], ["12748392", 45, 50, 5, 10]]
assessmentReport = AssessmentReport(name, headings, totals, returnedData)

#report = AssessmentReportRending(assessmentReport)


#Audit Report
headings = ["Date","Details"]
data = [["2014-04-14","Wrote rendering class"],["2014-04-14","Created Test Audit Log"],["2014-04-14","Inserted Test Data"],["2014-04-14","I hope this works"],["2014-04-14","How do you import classes?"],["2014-04-14","__init__"],["2014-04-14","If you see this then it worked"]]
testReport = AuditReport("Test report",headings, data)

#student mark report
studentNumber = "10189337"
_module = "COS332"
reportName = _module + " Student Marks Report for " + studentNumber 
headings = ["ST1", "ST2", "P1", "P2", "P3"]
totals = [50, 50, 10, 10, 10]
returnedData = [23, 45, 3, 7, 9]
studentReport = StudentMarksReport(reportName, headings, totals, returnedData)

#myCSVGen = CSVReportGenerator()
#test =myCSVGen.generateAssessmentReport("Cos332", "P1", "csv")

#myPDFGen = PDFReportGenerator()
#test = myPDFGen.generateAssessmentReport("Cos332", "P1", "pdf")


#dataOut = renderAuditReport(module, userID, alteredTable, dateFrom, dateTo)
fo = open("AuditReport.html","wb")
fo.write(bytes(dataOut))
fo.close()
print "Report Generated"
print "Saved to file 'AuditReport.html'"

dataOut = renderAssessmentReport("COS301", "Prac 1")
fo = open("AssessmentReport.html","wb")
fo.write(bytes(dataOut))
fo.close()

print "Report Generated"
print "Saved to file 'AssessmentReport.html'"


dataOut = renderStudentReport(studentReport)	
fo = open("StudentReport.html","wb")
fo.write(bytes(dataOut))
fo.close()

print "Report Generated"
print "Saved to file 'StudentReport.html'"
