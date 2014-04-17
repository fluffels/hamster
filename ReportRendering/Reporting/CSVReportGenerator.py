import csv
from datetime import datetime
from ReportRequest import ReportRequest
from ReportGenerator import ReportGenerator
from AuditReport import AuditReport
from StudentMarksReport import StudentMarksReport
from AssessmentReport import AssessmentReport

class CSVReportGenerator(ReportGenerator):
	def __init__(self):	
		#Constructor
		test = ""
    
	def genCSV(self,data,headings,name):
		self.doc_heading = name+".csv"
		fileName = self.doc_heading
		with open(fileName, 'wb') as csvOutput:
			filewriter = csv.writer(csvOutput, quoting=csv.QUOTE_ALL)
			filewriter.writerow(headings)
			filewriter.writerow(data)
  
  #return csvOutput

	def generateAssessmentReport(self, module, assessment):  #Assessment Report
		reportGenerator = WebReportGenerator()
		report = reportGenerator.generateAssessmentReport(module, assessment)
		
		reportname = "Assessmentcsv_" + module + datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
	      #INTEGRATE HERE
	      
	      #dataA = getAssessmentMarks(module,assessment)
	      #dataT = getTotals(module,assessment)
	      
	      #assign = AssessmentReport(reportname,dataA[0],dataT,dataA)
	      #header = merge(assign.getHeadings,assign.getotals)
	      
	 
	      #genCSV(assign.getData,header,assign.getReportName)
		self.genCSV([5,6,2],"Our header","test")
		#return assign.getReportName+".csv"
		return"test.csv"
	    
	    
	def generateStudentMarksReport(self, module, studentNo, assessments):  #Student Marks Report
		
	       reportGenerator = WebReportGenerator()
	       report = reportGenerator.generateStudentMarksReport(module, studentNo, assessments)
		
	      if assessments != "":
		dataA = getStudentMarks(module,studentNo, assessments)
		dataT = getTotals(module)
	      else:
		dataA = getStudentMarks(module,studentNo)
		dataT = getTotals(module)
	      
	      student = StudentMarksReport(name,headings,totals,data)
	      header = merge(student.getHeadings,student.getotals)
	      genCSV(student.getData,header,student.getReportName)
	      return student.getReportName+".csv"

	def generateAuditReport(self, module, userID, alteredTable, dateFrom, dateTo):  #Audit Report
	       reportGenerator = WebReportGenerator()
	       report = reportGenerator.generateAuditReport(userID, alteredTable, datefrom, dateTo)
		
	      if module != "":
		
		if userID != "":
		  
		  if alteredTable != "":
		    reportname = "Auditcsv_" + module + userID + alteredTable + datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		    #date = getUserTableAudit(module,userID,alteredTable,dateFrom,dateTo)
		  else:
		    reportname = "Auditcsv_" + module + userID + datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		    #data = getUserAudit(module,userID,dateFrom,dateTo) 
		else:
		  if alteredTable != "":
		    reportname = "Auditcsv_" + module + alteredTable + datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		    data = getTableAudit(module,alteredTable,dateFrom,dateTo)

	      audit = AuditReport(reportName,data[0],data)
	      genCSV(audit.getData(),audit.getHeadings(),audit.getReportName())
	      
	      return audit.getReportName() + ".csv"
	    
	def merge(self,header,total):
	    count=0
	    countb=0
	    listH = []
	    for i in header:
	      if count > 1:
		listH.append(i + "("+total[countb]+")")
	      listH.append(i);
	    return listH
	    


