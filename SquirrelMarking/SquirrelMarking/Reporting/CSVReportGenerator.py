import csv
from datetime import datetime
from ReportRequest import ReportRequest
from ReportGenerator import ReportGenerator
from AuditReport import AuditReport
from StudentMarksReport import StudentMarksReport
from AssessmentReport import AssessmentReport
from SquirrelMarking.businessLogicAPI import *
import StringIO

class CSVReportGenerator(ReportGenerator):
	def __init__(self):	
		#Constructor
		test = ""

	def genCSV(self,data,headings,name):
		#~ self.doc_heading = name+".csv"
		#~ fileName = self.doc_heading
		f = StringIO.StringIO()
		filewriter = csv.writer(f)
		filewriter.writerow(headings)
		filewriter.writerows(data)
		f.seek(0)
		return f
			
	def merging(self,header,total):
		count=0
		countb=0
		listH = []
		for i in header:
			if count > 1:
				listH.append(i + "("+total[countb]+")")
				listH.append(i)
		return listH

	def generateAssessmentReport(self, module, assessment):  #Assessment Report
		reportname = "Assessmentcsv_" + module

		returnData =[]
		name = []
		total = []
		mark = []

		people = getAllStudentsOfModule(module)
		for x in people:
			tempList = []
			tempList.append(x.getupId()[0])
			tempData = getAssessmentTotalForStudent(x.getupId(),module,assessment)
			for y in tempData:
				tempList.append(y[2])
			returnData.append(tempList)

		tempData = getAssessmentTotalForStudent(people[0].getupId(),module,assessment)
		name.append("uid")
		for y in tempData:
			name.append(y[0])
			total.append(y[1])
		reportName = module + " Assessment Report"
		assign = AssessmentReport(reportName,name,total,returnData)
		header = self.merging(name,total)
		tempCSV = self.genCSV(returnData,name,reportname)
		return tempCSV

	def generateStudentMarksReport(self, module, studentNo, assessments):  #Student Marks Report
		tempData = getAllAssessmentTotalsForStudent(studentNo,module)
		name = []
		total = []
		mark = []
		for x in tempData:
			name.append(x[0])
			total.append(x[1])
			mark.append(x[2])
		reportName = module + " Student Marks Report for " + studentNo 
		student = StudentMarksReport(reportName, name, total, mark)
		tempCSV = self.genCSV(mark,name,reportName)
		return tempCSV

	def generateAuditReport(self, module, userID, alteredTable, dateFrom, dateTo):  #Audit Report
		reportName = module + " Audit Report for "
		name = ""
		data = ""
		headings = []
		headings.append("PersonId")
		headings.append("Description")
		headings.append("AuditDescription")
		headings.append("Time")
		headings.append("TableName")
		headings.append("ColumnName")
		headings.append("OldValue")
		headings.append("NewValue")
		headings.append("AffectedRow")
		if module != "":
			
			if userID != "":
				
				if alteredTable != "":
					data = getUserTableAudit(module,userID,alteredTable,dateFrom,dateTo)
				else:
					data = getAuditLogFromTimeRangeAndUser(userID,dateFrom,dateTo) 
			else:
				if alteredTable != "":
					data = getTableAudit(module,alteredTable,dateFrom,dateTo)
		list = []
		
		for row in data:
			old_value = ""
			new_value = ""
			if row.old_value==None:
				old_value = "None"
			else:
				old_value = row.old_value
			if row.new_value==None:
				new_value = "None"
			else:
				new_value = row.new_value
			templist = []
			templist.append(row.person_id )
			templist.append(row.description )
			templist.append(row.action.auditDesc )
			templist.append(row.time.strftime("%Y-%m-%d %H:%M:%S"))
			templist.append(row.audit_table_id.tableName)
			templist.append(row.audit_table_column_id.columnName)
			templist.append(old_value)
			templist.append(new_value)
			templist.append(str(row.affected_row_id))
			list.append(templist)
		
		report = AuditReport(reportName, headings, list)
		tempCSV = self.genCSV(list,headings,reportName)

		return tempCSV


