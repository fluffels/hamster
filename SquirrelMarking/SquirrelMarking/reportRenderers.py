from Reporting.AssessmentReport import AssessmentReport
from Reporting.AuditReport import AuditReport
from Reporting.StudentMarksReport import StudentMarksReport
from Reporting.WebReportGenerator import *

def renderAuditReport(module, userID, alteredTable, dateFrom, dateTo):
	reportGenerator = WebReportGenerator()
	testReport = reportGenerator.generateAuditReport(module, userID, alteredTable, dateFrom, dateTo)
	htmlCode = "<div>"
	htmlCode += "<h1>" + testReport.getReportName() + "</h1>"
	htmlCode += "<table><tr>"
	for item in testReport.getHeadings():
		htmlCode += "<th>" + item + "</th>"
	htmlCode += "</tr>"
	for item in testReport.getData():
		htmlCode += "<tr>" 
		#for innerItem in item:
		htmlCode += "<td>" + str(item) + "</td>"
		htmlCode += '</tr>'
	htmlCode += "</table>"
	htmlCode += "</div>"
	return htmlCode

def  renderStudentReport(module, studentNo, assessments):
	reportGenerator = WebReportGenerator()
	studentReport = reportGenerator.generateStudentMarksReport(module, studentNo, assessments)
	htmlCode = "<div>"
	htmlCode += "<h1>" + studentReport.getReportName() + "</h1>"
	htmlCode += "<table><tr>"
	htmlCode += "<td>Assessment </td>"
	for item in studentReport.getHeadings():
		htmlCode += "<th>" + item + "</th>"
	htmlCode += "</tr>"
	htmlCode += "<tr>"
	htmlCode += "<td> Total marks </td>"
	for item in studentReport.getTotals():
		htmlCode += "<td>" + str(item) + "</td>"
	htmlCode += "</tr>"
	htmlCode += "<tr>"
	htmlCode += "<td>Student Mark</td>"
	for item in studentReport.getData():
		htmlCode += "<td>" + str(item) + "</td>"
	htmlCode += "</tr>"
	htmlCode += "</table><br/>"
	htmlCode += "</div>"
	return htmlCode

def renderAssessmentReport(module, assessment):
	reportGenerator = WebReportGenerator()
	assessmentReport = reportGenerator.generateAssessmentReport(module, assessment)
	htmlCode = "<div>"
	htmlCode += "<h2>Stats</h2>"
	htmlCode += "<br/><b>Student Marks </b>"
	htmlCode += "<table>"
	htmlCode += "<tr>"
	for item in assessmentReport.getHeadings():
		htmlCode += "<th>"+item+"</th>"
	htmlCode += "</tr>"
	htmlCode += "<tr>"
	htmlCode += "<td> Mean </td>"
	for item in assessmentReport.getAverage():
		htmlCode += "<td>" +str(item)+ "</td>"
	htmlCode += "</tr>"
	htmlCode += "</table><br/>"
	htmlCode += "<table>"
	htmlCode += "<tr>"
	htmlCode += "<td> Total marks </td>"
	for item in assessmentReport.getTotals():
		htmlCode += "<td>" + str(item)+ "</td>"
	htmlCode += "</tr>"
	htmlCode += "<tr>"
	for item in assessmentReport.getHeadings():
		htmlCode += "<th>"+item+"</th>"
	htmlCode += "</tr>"
	for item in assessmentReport.getData():
		htmlCode += "<tr>" 
		for innerItem in item:
			htmlCode += "<td>" + str(innerItem) + "</td>"
		htmlCode += '</tr>'
	htmlCode += "</table><br/>"
	htmlCode += "<div>"

	return htmlCode