from class_modules.StudentMarksReport import StudentMarksReport

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
