from class_modules.AuditReport import AuditReport

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