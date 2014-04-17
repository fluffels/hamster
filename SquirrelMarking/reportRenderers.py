from Reporting.AssessmentReport import AssessmentReport
from Reporting.StudentMarksReport import StudentMarksReport
from Reporting.AuditReport import AuditReport

def renderAuditReport(report):
	htmlCode = "<html><head><title> "+report.getReportName()+"</title></head><body>"
	htmlCode += "<h1>" + report.getReportName() + "</h1>"
	htmlCode += "<table><tr>"
	
	for item in report.getHeadings():
		htmlCode += "<th>" + item + "</th>"
	htmlCode += "</tr>"
	
	for item in report.getData():
		htmlCode += "<tr>" 
		for innerItem in item:
			htmlCode += "<td>" + str(innerItem) + "</td>"
		htmlCode += '</tr>'
	htmlCode += "</table>"
	
	htmlCode += "</body></html>"
	return htmlCode

def  renderStudentReport(report):
	htmlCode = "<html><head><title> "+report.getReportName()+"</title></head><body>"
	htmlCode += "<h1>" + report.getReportName() + "</h1>"
	
	htmlCode += "<table><tr>"
	htmlCode += "<td>Assessment </td>"
	for item in report.getHeadings():
		htmlCode += "<th>" + item + "</th>"
	htmlCode += "</tr>"
	
	htmlCode += "<tr>"
	htmlCode += "<td> Total marks </td>"
	for item in report.getTotals():
		htmlCode += "<td>" + str(item) + "</td>"
	htmlCode += "</tr>"
	
	
	htmlCode += "<tr>"
	htmlCode += "<td>Student Mark</td>"
	for item in report.getData():
		htmlCode += "<td>" + str(item) + "</td>"
	htmlCode += "</tr>"
	
	htmlCode += "</table><br/>"
	htmlCode += "</body></html>"
	
	return htmlCode

def renderAssessmentReport(report):
	htmlCode = "<html><head><title>AssessmentReport Name " +report.getName()+"</title></head><body>"
	htmlCode += "<h2>Stats</h2>"
	
	htmlCode += "<br/><b>Student Marks </b>"

	htmlCode += "<table>"
	htmlCode += "<tr>"
	for item in report.getHeadings():
		htmlCode += "<th>"+item+"</th>"
	htmlCode += "</tr>"

	htmlCode += "<tr>"
	htmlCode += "<td> Mean </td>"
	for item in report.getAverage():
		htmlCode += "<td>" +str(item)+ "</td>"
	htmlCode += "</tr>"

	#htmlCode += "<tr>"
	#htmlCode += "<td> Std Deviation </td>"
	#for item in report.getStdDeviation():
#		htmlCode += "<td>" + str(item) + "</td>"
#	htmlCode += "</tr>"
	htmlCode += "</table><br/>"

	htmlCode += "<table>"

	htmlCode += "<tr>"
	htmlCode += "<td> Total marks </td>"
	for item in report.getTotals():
		htmlCode += "<td>" + str(item)+ "</td>"
	htmlCode += "</tr>"

	htmlCode += "<tr>"
	for item in report.getHeadings():
		htmlCode += "<th>"+item+"</th>"
	htmlCode += "</tr>"

	for item in report.getData():
		htmlCode += "<tr>" 
		for innerItem in item:
			htmlCode += "<td>" + str(innerItem) + "</td>"
		htmlCode += '</tr>'

	htmlCode += "</table><br/>"
	htmlCode += "</body></html>"

	return htmlCode